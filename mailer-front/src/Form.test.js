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

test('can submit form and its validated', async () => {
    const form = render(<Form />);
    const senderEmail = getById(form.container, 'senderEmail');
    const receiverEmail = getById(form.container, 'receiverEmail');
    const emailSubject = getById(form.container, 'emailSubject');
    const message = getById(form.container, 'message');
    const submit = form.container.querySelector('button[type="submit"]');

    await wait(() => {
        fireEvent.change(senderEmail, {
            target: { value: 's@s.' },
        });
        fireEvent.blur(senderEmail);
    });
    expect(senderEmail).toHaveClass('error');

    await wait(() => {
        fireEvent.change(receiverEmail, {
            target: { value: 'r@r.' },
        });
        fireEvent.blur(receiverEmail);
    });
    expect(receiverEmail).toHaveClass('error');

    await wait(() => {
        fireEvent.change(emailSubject, {
            target: { value: '' },
        });
        fireEvent.blur(emailSubject);
    });
    expect(emailSubject).toHaveClass('error');

    await wait(() => {
        fireEvent.change(message, {
            target: { value: 'have a nice day' },
        });
    });

    await wait(() => {
        fireEvent.change(senderEmail, {
            target: { value: 's@s.com' },
        });
        fireEvent.blur(senderEmail);
    });
    expect(senderEmail).not.toHaveClass('error');

    await wait(() => {
        fireEvent.change(receiverEmail, {
            target: { value: 'r@r.dk' },
        });
        fireEvent.blur(receiverEmail);
    });
    expect(receiverEmail).not.toHaveClass('error');

    await wait(() => {
        fireEvent.change(emailSubject, {
            target: { value: 'hello there' },
        });
        fireEvent.blur(emailSubject);
    });
    expect(emailSubject).not.toHaveClass('error');

    await wait(() => {
        fireEvent.click(submit);
    });

    const infoBox = form.getByText(/Congrats! Your message was sent successfully/i);
    expect(infoBox).toBeInTheDocument();
  });

