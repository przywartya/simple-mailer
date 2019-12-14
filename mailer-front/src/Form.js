import React from 'react';

import { useFormik } from 'formik';

import './Form.css';


export function Form() {
    const [infoBox, setInfoBox] = React.useState('You can use this form to send email messages to anybody 🌎');
    const formik = useFormik({
        initialValues: {
            senderEmail: '',
            receiverEmail: '',
            emailSubject: '',
            message: ''
        },
        onSubmit: values => {
            setInfoBox(`Your message to ${formik.values.receiverEmail} was sent successfully 🥳`);
        },
    });

    return (
        <>
            <p>{infoBox}</p>
            <form id="simpleMailerForm" className="main-container__form" onSubmit={formik.handleSubmit}>
                <input
                    id="senderEmail"
                    name="senderEmail"
                    type="email"
                    placeholder="Sender's email"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.senderEmail}
                />
                <input
                    id="receiverEmail"
                    name="receiverEmail"
                    type="email"
                    placeholder="Receiver's email"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.receiverEmail}
                />
                <input
                    id="emailSubject"
                    name="emailSubject"
                    type="text"
                    placeholder="Subject"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.emailSubject}
                />
                <label htmlFor='message'>Your message goes here:</label>
                <textarea
                    id="message"
                    type="text"
                    name="message"
                    value={formik.values.message}
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                />
                <button type="submit">
                    Send
                </button>
            </form>
        </>
    );
}
