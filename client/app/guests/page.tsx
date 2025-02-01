'use client'

import { useState, useEffect } from 'react';
import { Guest } from '@/types/guest';
import AddGuestForm from "@/app/add_guest/AddGuestForm";

const GetGuestData = () => {
    const [response, setResponse] = useState([]);

    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/guest/all`)
            .then(res => res.json())
            .then(data => setResponse(data));
    }, []);

    return (
        <div className="d-flex justify-content-center table-responsive w-100 p-5">
            <table className="table table-striped table-dark w-50 rounded mr-10" style={{ overflow: 'hidden'}}>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                </tr>
                </thead>
                <tbody>
                {response ? (
                    response.map((guest: Guest) => (
                        <tr key={guest.id}>
                            <td>{guest.id}</td>
                            <td>{guest.first_name}</td>
                            <td>{guest.last_name}</td>
                        </tr>
                    ))
                ) : null}
                </tbody>
            </table>
            <AddGuestForm/>
        </div>
    )
};

export default GetGuestData;
