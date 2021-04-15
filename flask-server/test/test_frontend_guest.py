#-----------------------------------------------------------------------------
# test_frontend_guest.py
# 
# Frontend tests for the guest
#-----------------------------------------------------------------------------

from frontend import TestBase, SERVER_URL, SCHEDULE_HELP
import unittest

class TestGuest(TestBase):

    maxDiff = None
    url = SERVER_URL + '/schedule/asdofislerk'

    def test_header(self):
        self.header_test(check_button=False)

    def test_footer(self):
        self.footer_test(SCHEDULE_HELP)

    def test_text_components(self):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        header = scheduling_page.find_element_by_tag_name('h2')
        self.assertEqual(header.text, 'Scheduling with Erin Vuong')

        body = scheduling_page.find_element_by_tag_name('p')
        self.assertEqual(body.text, 'Does this time work for you?')

    def test_time_slot_carousel(self):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        date = 'Tuesday, March 23, 2021'
        times = ['09:00 AM to 10:00 AM', '10:00 AM to 11:00 AM', '01:00 PM to 02:00 PM']

        for i in range(2):
            for time in times:
                buttons = scheduling_page.find_elements_by_tag_name('button')
                self.assertEqual(len(buttons), 2)

                # check time slot information
                time_slot = buttons[0]
                self.assertEqual(time_slot.text, 
                    date + '\n' + time + '\nYes, this time works for me.')

                # check no button
                no = buttons[1]
                self.assertEqual(no.text, 'No, show me another time.')

                no.click() # move to next time

            # check last page
            body = scheduling_page.find_element_by_tag_name('p')
            self.assertEqual(body.text, 
                'It looks like there are no available times that work for you. ' + \
                'Please contact Erin Vuong to schedule your meeting.')

            button = scheduling_page.find_element_by_tag_name('button')
            self.assertEqual(button.text, 'Show me the times again.')

            button.click() # go back to beginning
        
    def test_open_confirm_form(self):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        time_slot = scheduling_page.find_element_by_tag_name('button')
        time_slot.click()

        modal = self.driver.find_element_by_class_name('modal-content')

        # check header
        header = modal.find_element_by_class_name('modal-header')

        title = header.find_element_by_class_name('modal-title')
        self.assertEqual(title.text, 'Confirm meeting')

        x_button = header.find_element_by_tag_name('button')
        spans = x_button.find_elements_by_tag_name('span')
        self.assertEqual(len(spans), 2)
        self.assertEqual(spans[0].text, '×')
        self.assertEqual(spans[1].text, 'Close')

        # check form
        form = modal.find_element_by_tag_name('form')

        # body
        body = form.find_element_by_class_name('modal-body')

        instructions = body.find_element_by_tag_name('p')
        self.assertEqual(instructions.text, 
            'Almost there! We just need a little more information to confirm your meeting.')

        form_groups = body.find_elements_by_class_name('form-group')
        self.assertEqual(len(form_groups), 3)

        labels = ['Name', 'Email address', 'Additional notes']
        infos = ['Please provide your name (first and last is preferred).',
                 'This will be used to send you meeting details. ' + \
                 'We\'ll never share your email with anyone else.',
                 'Anything you want to share with the meeting host.']
        placeholders = ['Name',
                        'email@example.com',
                        'Optional notes for the host...']
        textareas = [False, False, True]
        for i in range(len(form_groups)):
            self.check_simple_form_group(form_groups[i],
                                         labels[i],
                                         infos[i],
                                         placeholder=placeholders[i],
                                         textarea=textareas[i])

        # footer
        footer = form.find_element_by_class_name('modal-footer')
        buttons = footer.find_elements_by_tag_name('button')
        self.assertEqual(len(buttons), 2)
        self.assertEqual(buttons[0].text, 'Cancel')
        self.assertEqual(buttons[1].text, 'Schedule Meeting!')

    def test_closing_form_modal(self):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        # verify not faded
        fade = self.driver.find_elements_by_class_name('fade')
        self.assertEqual(len(fade), 0)

        time_slot = scheduling_page.find_element_by_tag_name('button')
        time_slot.click()
        
        # open modal
        modal = self.driver.find_element_by_class_name('modal-content')
        
        # verify scheduling page faded
        fade = self.driver.find_element_by_class_name('fade')

        # test x button
        header = modal.find_element_by_class_name('modal-header')
        x_button = header.find_element_by_tag_name('button')
        span = x_button.find_element_by_tag_name('span')
        self.assertEqual(span.text, '×')

        x_button.click()

        # verify not faded
        fade = self.driver.find_elements_by_class_name('fade')
        self.assertEqual(len(fade), 0)

        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        # open modal again
        time_slot = scheduling_page.find_element_by_tag_name('button')
        time_slot.click()
        
        modal = self.driver.find_element_by_class_name('modal-content')

        # verify scheduling page faded
        fade = self.driver.find_element_by_class_name('fade')

        # get cancel button
        cancel = modal.find_element_by_class_name('btn-secondary')
        self.assertEqual(cancel.text, 'Cancel')

        cancel.click()

        # verify not faded
        fade = self.driver.find_elements_by_class_name('fade')
        self.assertEqual(len(fade), 0)

    def test_form_validation(self):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        time_slot = scheduling_page.find_element_by_tag_name('button')
        time_slot.click()

        modal = self.driver.find_element_by_class_name('modal-content')

        # verify input checking not shown
        form_groups = modal.find_elements_by_class_name('form-group')
    
        for i in range(2):
            input_validation = form_groups[i].find_element_by_class_name(
                'invalid-feedback')
            self.assertEqual(input_validation.text, '')
            self.assertFalse(input_validation.is_displayed())

        submit_button = modal.find_element_by_class_name('btn-primary')
        self.assertEqual(submit_button.text, 'Schedule Meeting!')

        submit_button.click()

        # now input checking shown
        validations = ['Please provide a name.',
                       'Please provide a valid email address.']

        for i in range(2):
            input_validation = form_groups[i].find_element_by_class_name(
                'invalid-feedback')
            self.assertEqual(input_validation.text, validations[i])
            self.assertTrue(input_validation.is_displayed())

        # fill each of the forms and check that the validation goes away
        name = form_groups[0].find_element_by_tag_name('input') # name
        name.send_keys('Bobby Tables')

        name_validation = form_groups[0].find_element_by_class_name(
            'invalid-feedback')
        self.assertEqual(name_validation.text, '')
        self.assertFalse(name_validation.is_displayed())

        email = form_groups[1].find_element_by_tag_name('input') # email
        
        # invalid input entry
        email.send_keys('bobby')
        email_validation = form_groups[1].find_element_by_class_name(
            'invalid-feedback')
        self.assertEqual(email_validation.text, validations[1])
        self.assertTrue(email_validation.is_displayed())

        email.send_keys('bobby@tables.com')

        email_validation = form_groups[1].find_element_by_class_name(
            'invalid-feedback')
        self.assertEqual(email_validation.text, '')
        self.assertFalse(email_validation.is_displayed())

        # submit again and check submission now succeeds
        submit_button.click()

        # check the modal changed
        modal = self.driver.find_element_by_class_name('modal-content')
        title = modal.find_element_by_class_name('modal-title')
        self.assertEqual(title.text, 'Meeting confirmed!')

    def time_slot_confirm(self, index, date, time):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        # skip to right time slot
        no_button = scheduling_page.find_element_by_class_name('btn-outline-danger')
        for j in range(index):
            no_button.click()

        # open confirm form and submit
        time_slot = scheduling_page.find_element_by_tag_name('button')
        time_slot.click()

        modal = self.driver.find_element_by_class_name('modal-content')
        inputs = modal.find_elements_by_tag_name('input')
        name = inputs[0]
        email = inputs[1]

        name.send_keys('Bobby Tables')
        email.send_keys('bobby@tables.com')

        submit = modal.find_element_by_class_name('btn-primary')
        submit.click()

        # check confirmation modal
        modal = self.driver.find_element_by_class_name('modal-content')

        title = modal.find_element_by_class_name('modal-title')
        self.assertEqual(title.text, 'Meeting confirmed!')

        bodies = modal.find_elements_by_tag_name('p')
        self.assertEqual(len(bodies), 2)

        body = bodies[0]
        body_string = ('Your meeting for {} from {} has been confirmed. '
                       'Erin Vuong will contact you about meeting location '
                       'details. You should receive a confirmation email at '
                       'bobby@tables.com. To reschedule or cancel please contact'
                       ' Erin Vuong.')
        self.assertEqual(body.text, body_string.format(date, time))

        cal_msg = bodies[1]
        self.assertEqual(cal_msg.text, 
            'If you used a Google email address the event has been added ' + \
            'tenatively to your calendar.')

        done_button = modal.find_element_by_class_name('btn-primary')
        self.assertEqual(done_button.text, 'Done')
        done_button.click()

        # check final page
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')
        header = scheduling_page.find_element_by_tag_name('h2')
        self.assertEqual(header.text, 'Scheduling with Erin Vuong')
        
        body = scheduling_page.find_element_by_tag_name('p')
        self.assertEqual(body.text,
            'Thank you for scheduling! You can close this page now. ' + \
            'Check your email for meeting details.')

    def test_meeting_confirmed_all(self):
        date = 'Tuesday, March 23, 2021'
        times = ['09:00 AM to 10:00 AM', '10:00 AM to 11:00 AM', '01:00 PM to 02:00 PM']
        
        # test each time slot
        for i in range(3):
            self.time_slot_confirm(i, date, times[i])
            self.tearDown()
            self.setUp()

    def test_meeting_confirmed_x_button(self):
        scheduling_page = self.driver.find_element_by_class_name('scheduling-page')

        # open confirm form and submit
        time_slot = scheduling_page.find_element_by_tag_name('button')
        time_slot.click()

        modal = self.driver.find_element_by_class_name('modal-content')
        inputs = modal.find_elements_by_tag_name('input')
        name = inputs[0]
        email = inputs[1]

        name.send_keys('Bobby Tables')
        email.send_keys('bobby@tables.com')

        submit = modal.find_element_by_class_name('btn-primary')
        submit.click()

        # check confirmation modal
        modal = self.driver.find_element_by_class_name('modal-content')
        header = modal.find_element_by_class_name('modal-header')

        title = header.find_element_by_class_name('modal-title')
        self.assertEqual(title.text, 'Meeting confirmed!')

        x_button = header.find_element_by_tag_name('button')
        spans = x_button.find_elements_by_tag_name('span')
        self.assertEqual(len(spans), 2)
        self.assertEqual(spans[0].text, '×')
        self.assertEqual(spans[1].text, 'Close')

        # verify faded
        fade = self.driver.find_element_by_class_name('fade')

        x_button.click()

        # verify not faded
        fade = self.driver.find_elements_by_class_name('fade')
        self.assertEqual(len(fade), 0)

if __name__ == '__main__':
    unittest.main(warnings='ignore')