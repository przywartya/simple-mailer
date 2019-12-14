import React from 'react';
import { render, queryByAttribute, fireEvent, wait } from '@testing-library/react';
import { Form } from './Form';

const getById = queryByAttribute.bind(null, 'id');

test('renders all necessary fields', () => {
  const form = render(<Form />);

  const infoBox = form.getByText(/You can use this form to send email messages to anybody/i);
  expect(infoBox).toBeInTheDocument();

  const simpleMailerForm = getById(form.container, 'simpleMailerForm');
  expect(simpleMailerForm).toBeInTheDocument();

  const senderEmail = getById(form.container, 'senderEmail');
  expect(senderEmail).toBeInTheDocument();

  const receiverEmail = getById(form.container, 'receiverEmail');
  expect(receiverEmail).toBeInTheDocument();

  const emailSubject = getById(form.container, 'emailSubject');
  expect(emailSubject).toBeInTheDocument();

  const message = getById(form.container, 'message');
  expect(message).toBeInTheDocument();
});

test('can submit form', async () => {
    const form = render(<Form />);
    const senderEmail = getById(form.container, 'senderEmail');
    const receiverEmail = getById(form.container, 'receiverEmail');
    const emailSubject = getById(form.container, 'emailSubject');
    const message = getById(form.container, 'message');

    const submit = form.container.querySelector('button[type="submit"]');

    await wait(() => {
        fireEvent.change(senderEmail, {
            target: { value: 's@s.s' },
        });
    });
    await wait(() => {
        fireEvent.change(receiverEmail, {
            target: { value: 'r@r.r' },
        });
    });
    await wait(() => {
        fireEvent.change(emailSubject, {
            target: { value: 'hello there' },
        });
    });
    await wait(() => {
        fireEvent.change(message, {
            target: { value: 'have a nice day' },
        });
    });

    await wait(() => {
        fireEvent.click(submit);
    });

    const infoBox = form.getByText(/Your message to r@r.r was sent successfully/i);
    expect(infoBox).toBeInTheDocument();
  });

