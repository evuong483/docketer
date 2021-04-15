#-----------------------------------------------------------------------------
# test_frontend_host.py
# 
# Frontend tests for the host
#-----------------------------------------------------------------------------
from frontend import TestBase, SERVER_URL
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest
import time

class TestHomepage(TestBase):

    def test_header(self):
        self.header_test(False)

    def test_caption(self):
        landing_page = self.driver.find_element_by_class_name('landing-page')
        caption = landing_page.find_element_by_tag_name('h1')
        self.assertEqual(caption.text,
            'Intelligent scheduling with your preferences and productivity in mind.')

    def test_footer(self):
        self.footer_test()

class TestLoggedIn(TestBase):

    def login_logout(self):
        button = self.driver.find_element_by_id('login-button')
        button.click()

    def test_login_logout(self):
        # verify we're logged out
        self.driver.find_element_by_class_name('landing-page')

        # login
        self.login_logout()
        self.driver.find_element_by_class_name('user-page')

        # logout
        self.login_logout()
        self.driver.find_element_by_class_name('landing-page')

    def test_header_footer(self):
        self.login_logout()
        self.header_test(True)
        self.footer_test()

    def test_user_info(self):
        self.login_logout()
        time.sleep(0.5)

        user_info = self.driver.find_element_by_class_name('user-info')

        header = user_info.find_element_by_tag_name('h1')
        self.assertEqual(header.text, 'Hello, Erin!')

        body = user_info.find_element_by_tag_name('label')
        self.assertEqual(body.text, 'Your email is')

        email = user_info.find_element_by_tag_name('input')
        self.assertEqual(email.get_attribute('placeholder'),
                         'evuong@gmail.com')
        self.assertTrue(email.get_attribute('readOnly'))
        
    def check_generated_link(self, display):
        label = display.find_element_by_tag_name('label')
        self.assertEqual(
            label.text,
            'Share this one-time scheduling link to schedule a meeting!')

        link = display.find_element_by_tag_name('input')
        self.assertTrue(link.get_attribute('readOnly'))
        self.assertEqual(link.get_attribute('value'), 
                         SERVER_URL + '/schedule/os249DFdidl3')

        small = display.find_element_by_tag_name('small')
        self.assertEqual(
            small.text,
            ('Once the meeting is booked you will receive an email with details '
             'and it will be added to your integrated calendar.')
        )

    def test_link_generator_collapsed(self):
        self.login_logout()
        generator = self.driver.find_element_by_class_name('link-generator')
        
        header = generator.find_element_by_tag_name('h2')
        self.assertEqual(header.text, 'Generate a one-time scheduling link')

        # collapsed
        body = generator.find_element_by_tag_name('p')
        self.assertEqual(body.text,
            'A meeting can be scheduled up to 4 weeks in advance. Show advanced options.')

        rows = generator.find_elements_by_class_name('row')
        self.assertEqual(len(rows), 1)

        button = rows[0].find_element_by_tag_name('button')
        self.assertEqual(button.text, 'Generate link!')

        button.click()
        time.sleep(0.1)

        # check for form group and fields
        display = generator.find_element_by_class_name('form-group')
        self.check_generated_link(display)
       
    def test_link_generator_toggle(self):
        self.login_logout()
        generator = self.driver.find_element_by_class_name('link-generator')

        # collapsed
        body = generator.find_element_by_tag_name('p')
        self.assertEqual(body.text,
            'A meeting can be scheduled up to 4 weeks in advance. Show advanced options.')

        # expand
        link = body.find_element_by_tag_name('a')
        link.click()

        time.sleep(0.2)

        rows = generator.find_elements_by_class_name('row')
        self.assertEqual(len(rows), 6)

        # check form groups
        inputs = generator.find_elements_by_class_name('form-group')
        self.assertEqual(len(inputs), 8)
        del inputs[4]
        del inputs[6]
        self.assertEqual(len(inputs), 6)
        labels = ['Meeting length (in minutes)', 'Buffer time (in minutes)',
                  'Workday start time', 'Workday end time',
                  'Minimum days in advance', 'Up to this many weeks in advance']
        infos = ['How long should the meeting be?',
                 'How long should there be between this meeting and other events (before and after)?',
                 'What is the earliest time this meeting can start?',
                 'What is the latest time this meeting can end?',
                 'How many days in advance minimum should this meeting be scheduled?',
                 'How many weeks in advance can this meeting be scheduled (from ' + \
                 'today, regardless of when scheduling starts)?']
        values = ['60', '10', '09:00', '17:00', '1', '4']

        for i in range(len(inputs)):
            self.check_simple_form_group(inputs[i],
                                         labels[i],
                                         infos[i],
                                         values[i])

        link.click() # toggle

        time.sleep(0.2)

        # verify rows disappeared
        rows = generator.find_elements_by_class_name('row')
        self.assertEqual(len(rows), 1)

        button = rows[0].find_element_by_tag_name('button')
        self.assertEqual(button.text, 'Generate link!')

        button.click()
        time.sleep(0.1)

        # check for form group and fields
        display = generator.find_element_by_class_name('form-group')
        self.check_generated_link(display)

    def test_generated_link_copy(self):
        self.login_logout()

        time.sleep(0.1)

        # check for form group and fields
        generator = self.driver.find_element_by_class_name('link-generator')

        button = generator.find_element_by_class_name('btn-primary')
        self.assertEqual(button.text, 'Generate link!')
        
        button.click()
        time.sleep(0.1)
        
        display = generator.find_element_by_class_name('form-group')
        self.check_generated_link(display)
    
        copy_link = display.find_element_by_tag_name('a')
        copy_button = copy_link.find_element_by_class_name('fa-copy')

        # check hover
        tooltip = self.driver.find_elements_by_id('generated-copy-tooltip')
        self.assertEqual(len(tooltip), 0)

        builder = ActionChains(self.driver)
        builder.move_to_element(copy_button).perform()

        time.sleep(0.1)

        tooltip = self.driver.find_element_by_id('generated-copy-tooltip')
        inner = tooltip.find_element_by_class_name('tooltip-inner')
        self.assertEqual(inner.text, 'Copy')

        copy_link.click() # copy

        self.assertEqual(inner.text, 'Copied!')

        # check clipboard text
        self.driver.execute_script(
            '''window.open("{}/copy_help", "_blank");'''.format(SERVER_URL))
        self.driver.switch_to.window(self.driver.window_handles[-1])

        time.sleep(1)
        
        input = self.driver.find_element_by_tag_name('input')
        self.assertEqual(input.get_attribute('value'), '')

        input.send_keys(Keys.CONTROL, 'v')
        input.send_keys(Keys.ENTER)

        input = self.driver.find_element_by_tag_name('input')
        self.assertEqual(input.get_attribute('value'),
            'http://localhost:3000/schedule/os249DFdidl3')

    # TODO: test changing the options, check output?

    def test_preferences_default(self):
        self.login_logout()
        prefs = self.driver.find_element_by_class_name('parameter-controls')

         # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight - 1000);')

        # header
        header = prefs.find_element_by_tag_name('h3')
        self.assertEqual(header.text, 'Update preferences for Erin Vuong')

        instructions = prefs.find_element_by_tag_name('p')
        inst_str = ('These preferences are used during scheduling to try and '
                    'rank your available time slots by preferability. More '
                    'preferable time slots are then presented first to increase '
                    'the likelihood they are picked. We automatically prioritize'
                    ' time slots that don\'t fragment your existing unscheduled '
                    'time.')
        self.assertEqual(instructions.text, inst_str)

        # check form
        form = prefs.find_element_by_tag_name('form')

        form_groups = form.find_elements_by_class_name('form-group')
        self.assertEqual(len(form_groups), 2)

        # day
        day = form_groups[0]
        label = day.find_element_by_tag_name('label')
        self.assertEqual(label.text, 'Preferred scheduling day of the week')

        # check tooltip
        info = ('If you only had one meeting to schedule during the week, which '
                'day would you schedule it on?')
    
        tooltip = self.driver.find_elements_by_id('pref-weekdays-tooltip')
        self.assertEqual(len(tooltip), 0)

        icon = day.find_element_by_tag_name('svg')
        builder = ActionChains(self.driver)
        builder.move_to_element(icon).perform()

        time.sleep(0.1)

        tooltip = self.driver.find_element_by_id('pref-weekdays-tooltip')
        inner = tooltip.find_element_by_class_name('tooltip-inner')
        self.assertEqual(inner.text, info)

        # check select
        select = day.find_element_by_tag_name('select')

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']
        options = select.find_elements_by_tag_name('option')
        self.assertEqual(len(options), len(days))

        for i in range(len(options)):
            option = options[i]
            self.assertEqual(option.get_attribute('value'), str(i))
            self.assertEqual(option.text, days[i])

        # default value
        default = Select(select).first_selected_option.get_attribute('value')
        self.assertEqual(default, '2')
        
        # time
        hour = form_groups[1]
        label = hour.find_element_by_tag_name('label')
        self.assertEqual(label.text, 'Preferred scheduling hour of the day')
        
        info = ('If you only had one meeting to schedule during the workday, '
                'what time would you schedule it to start?')

        tooltip = self.driver.find_elements_by_id('pref-hour-tooltip')
        self.assertEqual(len(tooltip), 0)

        icon = hour.find_element_by_tag_name('svg')
        builder = ActionChains(self.driver)
        builder.move_to_element(icon).perform()

        time.sleep(0.1)

        tooltip = self.driver.find_element_by_id('pref-hour-tooltip')
        inner = tooltip.find_element_by_class_name('tooltip-inner')
        self.assertEqual(inner.text, info)

        # check select
        input = hour.find_element_by_tag_name('input')
        self.assertEqual(input.get_attribute('type'), 'time')
        self.assertEqual(input.get_attribute('value'), '10:00')

    # (check the defaults, check adding, deleting badges, 
    # remove all then add more/reload/etc)
    def test_outstanding_links_header(self):
        self.login_logout()

        time.sleep(0.1)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # header of outstanding
        outstanding = self.driver.find_element_by_class_name('outstanding-display')

        header = outstanding.find_element_by_tag_name('h2')
        self.assertEqual(header.text, 
                         'Here are your oustanding scheduling links.')

        bodies = outstanding.find_elements_by_tag_name('p')
        self.assertEqual(len(bodies), 3)
        self.assertEqual(bodies[0].text, 'You can copy or delete links here.')
        self.assertEqual(bodies[1].text,
            'Note that if you delete a link it can no longer be used for scheduling.')
        self.assertEqual(bodies[2].text,
            'Links will be deleted automatically once they have been used.')

    def test_outstanding_links_default(self):
        self.login_logout()

        time.sleep(0.1)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # check default links and tooltips
        outstanding = self.driver.find_element_by_class_name('outstanding-display')

        list_group = outstanding.find_element_by_class_name('list-group')
        items = list_group.find_elements_by_class_name('list-group-item')
        self.assertEqual(len(items), 2)

        base = 'http://localhost:3000/schedule/'
        targets = ['wo24SDFosdle', 'w8sfek39913f']

        for i in range(len(targets)):
            # check link
            self.assertEqual(items[i].text, base + targets[i])

    def test_outstanding_links_delete_only(self):
        self.login_logout()

        time.sleep(0.1)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        outstanding = self.driver.find_element_by_class_name('outstanding-display')
        list_group = outstanding.find_element_by_class_name('list-group')

        # delete one link
        first = list_group.find_element_by_class_name('list-group-item')

        links = first.find_elements_by_tag_name('a')
        self.assertEqual(len(links), 2)

        x_button = links[1].find_element_by_tag_name('svg')

        # check hover
        tooltip = self.driver.find_elements_by_id('wo24SDFosdle-delete-tooltip')
        self.assertEqual(len(tooltip), 0)

        builder = ActionChains(self.driver)
        builder.move_to_element(x_button).perform()

        time.sleep(0.1)

        tooltip = self.driver.find_element_by_id('wo24SDFosdle-delete-tooltip')
        inner = tooltip.find_element_by_class_name('tooltip-inner')
        self.assertEqual(inner.text, 'Delete')

        # Delete and check badge
        badge = first.find_elements_by_class_name('badge-danger')
        self.assertEqual(len(badge), 0) # verify no badge

        links[1].click()

        badge = first.find_element_by_class_name('badge-danger')
        self.assertEqual(badge.text, 'Deleted')

        # Reload and check there's only one
        self.driver.refresh()

        time.sleep(0.1)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        outstanding = self.driver.find_element_by_class_name('outstanding-display')
        list_group = outstanding.find_element_by_class_name('list-group')

        # only one!
        elements = list_group.find_elements_by_class_name('list-group-item')
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].text, 
                         'http://localhost:3000/schedule/w8sfek39913f')

    def test_outstanding_links_delete_add(self):
        self.login_logout()

        time.sleep(0.3)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        outstanding = self.driver.find_element_by_class_name('outstanding-display')
        list_group = outstanding.find_element_by_class_name('list-group')

        # delete all links
        elements = list_group.find_elements_by_class_name('list-group-item')

        for element in elements:
            links = element.find_elements_by_tag_name('a')
            x_button = links[1].find_element_by_tag_name('svg')
            x_button.click()
            time.sleep(0.5)

        # refresh and check no viewer
        self.driver.refresh()

        time.sleep(1)

        outstanding = self.driver.find_elements_by_class_name('outstanding-display')
        self.assertEqual(len(outstanding), 0)

        # generate new link, should reappear
        link_gen = self.driver.find_element_by_class_name('link-generator')
        submit = link_gen.find_element_by_tag_name('button')
        self.assertEqual(submit.text, 'Generate link!')

        submit.click()
        time.sleep(0.1)

        outstanding = self.driver.find_element_by_class_name('outstanding-display')
        list_group = outstanding.find_element_by_class_name('list-group')

        elements = list_group.find_elements_by_class_name('list-group-item')
        self.assertEqual(len(elements), 1)

         # should be added to the top
        new = elements[0]
        self.assertEqual(new.text, 'http://localhost:3000/schedule/os249DFdidl3 New')

    def test_outstanding_links_new_only(self):
        self.login_logout()

        # check only 2 links so far
        time.sleep(0.1)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        outstanding = self.driver.find_element_by_class_name('outstanding-display')
        list_group = outstanding.find_element_by_class_name('list-group')

        elements = list_group.find_elements_by_class_name('list-group-item')
        self.assertEqual(len(elements), 2)

        # generate new link
        link_gen = self.driver.find_element_by_class_name('link-generator')
        submit = link_gen.find_element_by_tag_name('button')
        self.assertEqual(submit.text, 'Generate link!')

        submit.click()
        time.sleep(0.1)

        elements = list_group.find_elements_by_class_name('list-group-item')
        self.assertEqual(len(elements), 3)

        # should be added to the top
        new = elements[0]
        self.assertEqual(new.text, 'http://localhost:3000/schedule/os249DFdidl3 New')

        badge = new.find_element_by_class_name('badge-success')
        self.assertEqual(badge.text, 'New')

    def test_outstanding_links_copy_only(self):
        self.login_logout()

        time.sleep(0.1)

        # scroll to bottom
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        outstanding = self.driver.find_element_by_class_name('outstanding-display')
        list_group = outstanding.find_element_by_class_name('list-group')

        # copy one link
        first = list_group.find_element_by_class_name('list-group-item')

        links = first.find_elements_by_tag_name('a')
        self.assertEqual(len(links), 2)

        copy_button = links[0].find_element_by_class_name('fa-copy')

        # check hover
        tooltip = self.driver.find_elements_by_id('wo24SDFosdle-copy-tooltip')
        self.assertEqual(len(tooltip), 0)

        builder = ActionChains(self.driver)
        builder.move_to_element(copy_button).perform()

        time.sleep(0.1)

        tooltip = self.driver.find_element_by_id('wo24SDFosdle-copy-tooltip')
        inner = tooltip.find_element_by_class_name('tooltip-inner')
        self.assertEqual(inner.text, 'Copy')

        links[0].click() # copy

        self.assertEqual(inner.text, 'Copied!')

        # check clipboard text
        self.driver.execute_script(
            '''window.open("{}/copy_help", "_blank");'''.format(SERVER_URL))
        self.driver.switch_to.window(self.driver.window_handles[-1])

        time.sleep(1)
        
        input = self.driver.find_element_by_tag_name('input')
        self.assertEqual(input.get_attribute('value'), '')

        input.send_keys(Keys.CONTROL, 'v')
        input.send_keys(Keys.ENTER)

        input = self.driver.find_element_by_tag_name('input')
        self.assertEqual(input.get_attribute('value'),
            'http://localhost:3000/schedule/wo24SDFosdle')

if __name__ == '__main__':
    unittest.main(warnings='ignore')