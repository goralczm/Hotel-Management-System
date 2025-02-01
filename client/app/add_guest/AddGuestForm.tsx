'use client'

import axios from 'axios';
import {useEffect, useState} from 'react';
import { Guest } from '@/types/guest';

const PostGuestData = () => {
    const [response, setResponse] = useState(null);

    const [formValues, setFormValues] = useState({
        id: 0,
        first_name: "",
        last_name: "",
        email: "",
        address: "",
        city: "",
        country: "",
        zip_code: "",
        phone_number: "",
        accessibility_option_ids: [-1],
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormValues((prevValues) => ({
            ...prevValues,
            [name]: value,
        }));
    };

    const onSubmit = (event) => {
        event.preventDefault();

        const guest = { ...formValues };

        setFormValues({
            id: 0,
            first_name: "",
            last_name: "",
            email: "",
            address: "",
            city: "",
            country: "",
            zip_code: "",
            phone_number: "",
            accessibility_option_ids: [-1],
        });

        sendGuestData(guest);
    };

    const sendGuestData = async (guest: string) => {
        const payload = {
            "guest": guest,
            accessibility_option_ids: [-1],
        };

        try {
            const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/guest/create`, payload, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            setResponse(res.data);
            console.log('Response:', res.data);
        } catch (error) {
            console.error('Error sending guest data:', error);
        }

        window.location.reload();
    };

    return (
        <div className="d-flex justify-content-center align-items-center w-50">
            <div className="container border rounded p-5">
                <form className="row g-3" onSubmit={onSubmit}>
                    <div className="col-md-6">
                        <label htmlFor="first_name" className="form-label">First Name</label>
                        <input type="text" className="form-control" id="first_name" name="first_name"
                               placeholder="John" onChange={handleInputChange}/>
                    </div>
                    <div className="col-md-6">
                        <label htmlFor="last_name" className="form-label">Last Name</label>
                        <input type="text" className="form-control" id="last_name" name="last_name" placeholder="Doe" onChange={handleInputChange}/>
                    </div>
                    <div className="col-12">
                        <label htmlFor="email" className="form-label">Email</label>
                        <input type="email" className="form-control" id="email" name="email"
                               placeholder="john.doe@example.com" onChange={handleInputChange}/>
                    </div>
                    <div className="col-12">
                        <label htmlFor="address" className="form-label">Address</label>
                        <input type="text" className="form-control" id="address" name="address"
                               placeholder="1234 Main St" onChange={handleInputChange}/>
                    </div>
                    <div className="col-md-6">
                        <label htmlFor="city" className="form-label">City</label>
                        <input type="text" className="form-control" id="city" name="city" placeholder="Metropolis" onChange={handleInputChange}/>
                    </div>
                    <div className="col-md-4">
                        <label htmlFor="country" className="form-label">Country</label>
                        <input type="text" className="form-control" id="country" name="country"
                               placeholder="Wonderland" onChange={handleInputChange}/>
                    </div>
                    <div className="col-md-2">
                        <label htmlFor="zip_code" className="form-label">Zip</label>
                        <input type="text" className="form-control" id="zip_code" name="zip_code" placeholder="12345" onChange={handleInputChange}/>
                    </div>
                    <div className="col-md-12">
                        <label htmlFor="phone_number" className="form-label">Phone Number</label>
                        <input type="text" className="form-control" id="phone_number" name="phone_number"
                               placeholder="123-456-7890" onChange={handleInputChange}/>
                    </div>
                    <div className="col-12">
                        <button type="submit" className="btn btn-primary">Sign In</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default PostGuestData;
