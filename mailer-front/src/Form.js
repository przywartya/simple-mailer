import axios from "axios";
import React from "react";

import { useFormik } from "formik";
import TextTransition, { presets } from "react-text-transition";

import { isEmpty } from "./utils";

import "./Form.css";

const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;

const validate = values => {
    const errors = {};

    if (!values.emailSubject) {
        errors.emailSubject = "Required";
    }

    const emailFields = ["senderEmail", "receiverEmail"];

    emailFields.forEach(field => {
        if (!values[field]) {
            errors[field] = "Required";
        } else if (!emailRegex.test(values[field])) {
            errors[field] = "Invalid email address";
        }
    });

    return errors;
};

export function Form() {
    const defaultInfoBox =
        "You can use this form to send email messages to anybody 🌎";
    const [infoBox, setInfoBox] = React.useState(defaultInfoBox);
    const formik = useFormik({
        initialValues: {
            senderEmail: "",
            receiverEmail: "",
            emailSubject: "",
            message: ""
        },
        validate,
        onSubmit: async values => {
            try {
                await axios.post("http://localhost:8080/mail", values);
                setInfoBox(`Congrats! Your message was sent successfully 🥳`);
                formik.resetForm();
            } catch (err) {
                console.error(err);
                setInfoBox(`We are sorry, something went wrong 🤧`);
            } finally {
                setTimeout(() => {
                    setInfoBox(defaultInfoBox);
                }, 4000);
            }
        }
    });

    return (
        <>
            <div className="main-container__info-box">
                <TextTransition text={infoBox} springConfig={presets.wobbly} />
            </div>
            <form
                id="simpleMailerForm"
                className="main-container__form"
                onSubmit={formik.handleSubmit}
            >
                <input
                    id="senderEmail"
                    name="senderEmail"
                    type="email"
                    placeholder="Sender's email"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.senderEmail}
                    className={
                        formik.touched.senderEmail && formik.errors.senderEmail
                            ? "error"
                            : ""
                    }
                />
                <input
                    id="receiverEmail"
                    name="receiverEmail"
                    type="email"
                    placeholder="Receiver's email"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.receiverEmail}
                    className={
                        formik.touched.receiverEmail &&
                        formik.errors.receiverEmail
                            ? "error"
                            : ""
                    }
                />
                <input
                    id="emailSubject"
                    name="emailSubject"
                    type="text"
                    placeholder="Subject"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.emailSubject}
                    className={
                        formik.touched.emailSubject &&
                        formik.errors.emailSubject
                            ? "error"
                            : ""
                    }
                />
                <label htmlFor="message">Your message goes here:</label>
                <textarea
                    id="message"
                    type="text"
                    name="message"
                    value={formik.values.message}
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                />
                <button
                    type="submit"
                    disabled={
                        formik.touched.senderEmail &&
                        formik.touched.receiverEmail &&
                        formik.touched.emailSubject &&
                        !isEmpty(formik.errors)
                    }
                >
                    Send
                </button>
            </form>
        </>
    );
}
