import axios from "axios";
import React from "react";

import { useFormik } from "formik";
import TextTransition, { presets } from "react-text-transition";

import { isEmpty } from "./utils";

import "./Form.css";

const formFields = [
    { id: "senderEmail", type: "email", placeholder: "Sender's email" },
    { id: "receiverEmail", type: "email", placeholder: "Receiver's email" },
    { id: "emailSubject", type: "text", placeholder: "Subject" },
    { id: "message", type: "textarea", placeholder: "Your message goes here:" }
];

const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;

function validate(values) {
    const errors = {};
    formFields.forEach(({ id, type }) => {
        if (!values[id]) {
            errors[id] = "Required";
        } else if (type === "email" && !emailRegex.test(values[id])) {
            errors[id] = "Invalid email address";
        }
    });
    return errors;
}

export function Form() {
    const defaultInfoBox =
        "You can use this form to send email messages to anybody 🌎";
    const [infoBox, setInfoBox] = React.useState(defaultInfoBox);
    const formik = useFormik({
        initialValues: formFields.reduce((prev, { id }) => {
            prev[id] = "";
            return prev;
        }, {}),
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

    const submitDisabled =
        formik.touched.senderEmail &&
        formik.touched.receiverEmail &&
        formik.touched.emailSubject &&
        formik.touched.message &&
        !isEmpty(formik.errors);

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
                {formFields.map(({ id, type, placeholder }) => (
                    <Field
                        formik={formik}
                        key={id}
                        fieldName={id}
                        fieldType={type}
                        placeholder={placeholder}
                    />
                ))}
                <button type="submit" disabled={submitDisabled}>
                    Send
                </button>
            </form>
        </>
    );
}

function Field({ formik, fieldName, fieldType, placeholder }) {
    if (fieldType === "textarea") {
        return (
            <>
                <label htmlFor={fieldName}>{placeholder}</label>
                <textarea
                    type="text"
                    id={fieldName}
                    name={fieldName}
                    value={formik.values[fieldName]}
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                />
            </>
        );
    }
    return (
        <input
            id={fieldName}
            name={fieldName}
            type={fieldType}
            placeholder={placeholder}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values[fieldName]}
            className={
                formik.touched[fieldName] && formik.errors[fieldName]
                    ? "error"
                    : ""
            }
        />
    );
}
