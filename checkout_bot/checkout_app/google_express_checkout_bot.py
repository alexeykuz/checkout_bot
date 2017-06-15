# -*- coding: utf-8 -*-
import logging
import os
import time

from django.conf import settings

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from checkout_app.models import ProductOrder, STATE_ERROR, \
    STATE_IN_PROCESS, STATE_SOLD_OUT, STATE_SUCCESS_FINISHED

logger = logging.getLogger('google_express_logger')


class GoogleExpressCheckoutBot(object):
    accounts_url = 'https://accounts.google.com'
    email = 'alex@halevienterprises.com'
    password = 'nochum12'

    cart_url = 'https://www.google.com/express/cart'
    google_express_url = 'https://www.google.com/express/'
    goods_url = 'https://www.google.com/express/u/0/product/' \
        '9182472493455614380_10269187404013219762_9090995?' \
        'ei=v1InWZDxHtKwigOy64PIDw&ved=0EOEqCA8'

    product_order = None

    user_is_authenticated = False

    def __init__(self, order_id=None, *args, **kwargs):
        os.environ["DISPLAY"] = ":1085"

        self.browser = webdriver.Chrome(
            executable_path=settings.DRIVER_PATH,
            service_args=["--verbose", "--log-path=/tmp/chrome.log"])
        self.browser.set_window_size(1024, 768)

        try:
            self.product_order = ProductOrder.objects.get(pk=order_id)
            self.product_order.status = STATE_IN_PROCESS
            self.product_order.save()
            logger.warn('Product order ID: ' + str(self.product_order.id))
        except ProductOrder.DoesNotExist as e:
            logger.error(e)

    def place_an_order(self):
        """Make order for specified goods
        """
        if self.product_order:
            self._make_login()
            self._clean_cart_list()
            self._set_delivery_address()
            self._add_order()

        self._close_selenium_browser()

    def _make_login(self):
        """Try to authenticate with selenium browser
        """
        self.browser.get(self.accounts_url)

        self._post_email_with_selenium()
        self._post_password_with_selenium()
        self._set_if_user_authenticated()

    def _post_email_with_selenium(self):
        def wait_sign_in_page_load():
            element_exists = self._selenium_element_load_waiting(
                By.ID, 'identifierId',
                success_msg='Sign in page loaded',
                timeout_exception_msg='Timed out waiting Sign in page open')
            if element_exists:
                return True

        try:
            page_loaded = wait_sign_in_page_load()
            if not page_loaded:
                self._go_to_login_from_accounts_page()
                wait_sign_in_page_load()

            email = self.browser.find_element_by_id('identifierId')
            email.send_keys(self.email)
            button_next = self.browser.find_element_by_id('identifierNext')
            button_next.click()
        except Exception as e:
            logger.error(e)

    def _go_to_login_from_accounts_page(self):
        def wait_accounts_page_load():
            self._selenium_element_load_waiting(
                By.ID, 'identifierLink',
                success_msg='Accounts page loaded',
                timeout_exception_msg='Timed out waiting Accounts page open')

        try:
            wait_accounts_page_load()
            identifier_link = self.browser.find_element_by_id('identifierLink')
            identifier_link.click()
        except Exception as e:
            logger.error(e)

    def _post_password_with_selenium(self):
        def wait_password_page_load():
            self._selenium_element_load_waiting(
                By.NAME, 'password',
                success_msg='Password page loaded',
                timeout_exception_msg='Timed out waiting Password page open')

        try:
            wait_password_page_load()
            password = self.browser.find_element_by_name('password')
            password.send_keys(self.password)
            button_next = self.browser.find_element_by_id('passwordNext')
            button_next.click()
        except Exception as e:
            logger.error(e)

    def _set_if_user_authenticated(self):
        exception_msg = 'Timed out waiting for user authenticated page'
        elem_exists = self._selenium_element_load_waiting(
            By.CLASS_NAME, 'gbii',
            success_msg='User authenticated',
            timeout_exception_msg=exception_msg)

        if elem_exists:
            self.user_is_authenticated = True

    def _clean_cart_list(self):
        while True:
            time.sleep(10)
            self.browser.get(self.cart_url)
            self._remove_item_from_cart()
            if self._is_cart_empty():
                break

    def _remove_item_from_cart(self):
        xpath = '//div[contains(@class, "cartItemOptions")][1]/a'

        def wait_cart_items_load():
            excp_msg = 'Timed out waiting Remove item button load'
            self._selenium_element_load_waiting(
                By.XPATH, xpath,
                success_msg='Remove item button loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_cart_items_load()
            remove_item_link = self.browser.find_element_by_xpath(xpath)
            remove_item_link.click()
        except Exception as e:
            logger.error(e)

    def _is_cart_empty(self):
        try:
            cart_is_empty = self.browser.find_elements_by_class_name(
                'emptyCartMessageWrapper')
            if cart_is_empty:
                logger.info('Message "Cart is empty" displayed')
                return True
        except Exception as e:
            logger.error(e)
            return False

    def _set_delivery_address(self):
        self.browser.get(self.google_express_url)
        self._open_address_dropdown_menu()
        self._open_address_popup()
        self._press_edit_address_link()
        self._update_address()
        self._select_first_from_address_list()

    def _open_address_dropdown_menu(self):
        def wait_dropdown_menu_load():
            excp_msg = 'Timed out waiting for dropdown menu load'
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'addressDeliverToZipLabel',
                success_msg='Dropdown menu loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_dropdown_menu_load()
            show_popup_button = self.browser.find_element_by_class_name(
                'addressDeliverToZipLabel')
            show_popup_button.click()
        except Exception as e:
            logger.error(e)

    def _open_address_popup(self):
        xpath = '//ul[contains(@class, "addressSelectorDropdown")]/li/button'

        def wait_change_address_button_load():
            excp_msg = 'Timed out waiting for change address button load'
            self._selenium_element_load_waiting(
                By.XPATH, xpath, success_msg='Change address button loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_change_address_button_load()
            change_address_button = self.browser.find_element_by_xpath(xpath)
            change_address_button.click()
        except Exception as e:
            logger.error(e)

    def _press_edit_address_link(self):
        xpath = '//div[contains(@class, "addressButtonArea")]/' \
            'button/span[contains(text(),"edit")][1]'

        def wait_edit_address_link_load():
            excp_msg = 'Timed out waiting for edit address link load'
            self._selenium_element_load_waiting(
                By.XPATH, xpath,
                success_msg='Edit address link loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_edit_address_link_load()
            edit_address_link = self.browser.find_element_by_xpath(xpath)
            edit_address_link.click()
        except Exception as e:
            logger.error(e)

    def _update_address(self):
        def wait_edit_address_popup_load():
            excp_msg = 'Timed out waiting for address form load'
            self._selenium_element_load_waiting(
                By.NAME, 'addressForm',
                success_msg='Address form loaded',
                timeout_exception_msg=excp_msg)

        def send_recipient_order_name():
            recipient_order_name = self.browser.find_element_by_name('name')
            recipient_order_name.clear()
            recipient_order_name.send_keys(self.product_order.product_buyer)

        def send_address():
            address = self.browser.find_element_by_xpath(
                '//input[@name="address"]')
            address.clear()
            address.send_keys(self.product_order.buyer_address)

        def send_city():
            city = self.browser.find_element_by_name('city')
            city.clear()
            city.send_keys(self.product_order.buyer_city)

        def send_state():
            xpath = '//md-option[@value="' + \
                self.product_order.buyer_state_code + '"]'

            def wait_state_popup_load():
                excp_msg = 'Timed out waiting for state popup load'
                self._selenium_element_load_waiting(
                    By.XPATH, xpath,
                    success_msg='State popup loaded',
                    timeout_exception_msg=excp_msg)

            state_field = self.browser.find_element_by_name('state')
            state_field.click()
            wait_state_popup_load()
            state_option = self.browser.find_element_by_xpath(xpath)
            state_option.click()

        def send_postal_code():
            postal_code = self.browser.find_element_by_name('postalCode')
            postal_code.clear()
            postal_code.send_keys(self.product_order.buyer_postal_code)

        save_button_xpath = '//form[@name="addressForm"]/' \
            'md-dialog-actions/button[@type="submit"]'

        try:
            wait_edit_address_popup_load()
            send_recipient_order_name()
            send_address()
            send_city()
            send_postal_code()
            send_state()
            time.sleep(2)
            button_save = self.browser.find_element_by_xpath(save_button_xpath)
            button_save.click()
        except Exception as e:
            logger.error(e)

    def _select_first_from_address_list(self):
        xpath = '//md-list-item[contains(@class, "addressOption")][1]/' \
            'div/gsx-address-content'

        def wait_change_address_popup_load():
            excp_msg = 'Timed out waiting for change address popup load'
            self._selenium_element_load_waiting(
                By.XPATH, xpath,
                success_msg='Change address popup loaded',
                timeout_exception_msg=excp_msg)

        try:
            wait_change_address_popup_load()
            edit_address_link = self.browser.find_element_by_xpath(xpath)
            edit_address_link.click()
        except Exception as e:
            logger.error(e)

    def _add_order(self):
        self.browser.get(self.goods_url)

        goods_sold_out = self._check_goods_sold_out()

        if self.user_is_authenticated and not goods_sold_out:
            self._add_goods_to_cart()
            self._go_to_shopping_cart_and_checkout()
            self._press_on_place_order_button()
            self._is_order_confirmation_container()

    def _check_goods_sold_out(self):
        exc_msg = 'Timed out waiting for Sold out text load'

        def wait_sold_out_entry():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'soldOutText',
                success_msg='Sold out text loaded',
                timeout_exception_msg=exc_msg)

        try:
            wait_sold_out_entry()
            self.browser.find_element_by_class_name('soldOutText')
            self.product_order.status = STATE_SOLD_OUT
            self.product_order.save()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def _add_goods_to_cart(self):
        def wait_add_to_cart_button_load():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'addItemButton',
                success_msg='Add item button loaded',
                timeout_exception_msg='Timed out waiting for Add item button')

        try:
            wait_add_to_cart_button_load()
            add_item_button = self.browser.find_element_by_class_name(
                'addItemButton')
            add_item_button.click()
        except Exception as e:
            logger.error(e)

    def _go_to_shopping_cart_and_checkout(self):
        def wait_cart_page_load():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'checkoutButton',
                success_msg='Cart page loaded',
                timeout_exception_msg='Timed out waiting Cart page open')

        try:
            self.browser.get(self.cart_url)
            wait_cart_page_load()
            checkout_button = self.browser.find_element_by_class_name(
                'checkoutButton')
            checkout_button.click()
        except Exception as e:
            logger.error(e)

    def _press_on_place_order_button(self):
        def wait_submit_order_button_load():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'submitOrderButton',
                success_msg='Submit order button loaded',
                timeout_exception_msg='Timed out waiting Submit order button')

        try:
            wait_submit_order_button_load()
            submit_order_button = self.browser.find_element_by_class_name(
                'submitOrderButton')
            submit_order_button.click()
        except Exception as e:
            logger.error(e)

    def _is_order_confirmation_container(self):
        exc_msg = 'Timed out waiting Order confirmation container'

        def wait_order_confirmation_container_load():
            self._selenium_element_load_waiting(
                By.CLASS_NAME, 'orderConfirmationContainer',
                success_msg='Order confirmation container loaded',
                timeout_exception_msg=exc_msg)

        try:
            wait_order_confirmation_container_load()
            order_confirmation = self.browser.find_element_by_class_name(
                'orderConfirmationContainer')
            if order_confirmation:
                self.product_order.status = STATE_SUCCESS_FINISHED
        except Exception as e:
            logger.error(e)
            self.product_order.status = STATE_ERROR

        self.product_order.save()

    def _close_selenium_browser(self):
        try:
            self.browser.close()
            self.browser.quit()
            logger.info('Browser closed')
        except OSError as e:
            logger.error(e)

    def _selenium_element_load_waiting(
            self, by_selector_type, selector,
            success_msg='', timeout_exception_msg=''):
        """Wrapper around explicity waiting for
        elememt will appear in selenium browser
        """
        try:
            element_present = EC.visibility_of_element_located(
                (by_selector_type, selector))
            WebDriverWait(
                self.browser, settings.TIMEOUT_PAGE_LAODING).until(
                    element_present)
            logger.info(success_msg)
        except TimeoutException:
            logger.error(timeout_exception_msg)
            return False
        except Exception as e:
            logger.error(e)
            return False

        return True

    def save_page_to_log_if_debug(self, file_name, debug=False):
        # Write html pages to project logs dir if DEBUG setting is True
        if settings.DEBUG or debug:
            file_path = '%s/%s' % (
                settings.LOGS_DIR, file_name.replace(' ', '_'))
            logger.info('Path to employees list html file: %s' % file_path)
            try:
                page = self.browser.page_source.encode('utf-8')
            except Exception as e:
                logger.error(e)
                return None

            with open(file_path, 'w') as f:
                f.write(page)

    def save_img_to_log_if_debug(self, file_name, debug=False):
        # Save screenshot into logs dir if DEBUG setting is True
        if settings.DEBUG or debug:
            try:
                self.browser.save_screenshot(file_name)
            except Exception as e:
                logger.error(e)
