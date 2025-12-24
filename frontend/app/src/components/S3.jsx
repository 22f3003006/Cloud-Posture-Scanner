import React, { use } from 'react'
import './S3.css'
import axios from 'axios'
import { useState, useEffect } from 'react'
function S3() {
    const [buckets, setBuckets] = useState([])
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/buckets')
        .then(response => {
            setBuckets(response.data)
        })
    }, [])
    return (
        <div className="box">
            <h2>S3 Buckets</h2>
            {buckets.length === 0 ? (
                <p style={{ fontStyle: 'italic', textAlign: 'center', marginTop: '2rem'}}>Loading, Please Wait....</p>
            ) :
                <table border="1">
                    <thead>
                    <tr>
                        <th>Bucket Name</th>
                        <th>Creation Date</th>
                        <th>Region</th>
                        <th>Encryption </th>
                        <th>Access Policy-Public</th>
                    </tr>
                    </thead>
                    <tbody>
                    {buckets.map(b => (
                        <tr key={b.BucketName}>
                            <td>{b.BucketName}</td>
                            <td>{b.CreationDate}</td>
                            <td>{b.Region}</td>
                            <td>
                                {b.Encryption && b.Encryption.Rules
                                    ? b.Encryption.Rules.map(r => r.ApplyServerSideEncryptionByDefault.SSEAlgorithm).join(", ")
                                    : "None"}
                                </td>
                            <td>{b.AccessPolicyPublic ? "True" : "False"}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            }
        </div>
    )
}
export default S3;