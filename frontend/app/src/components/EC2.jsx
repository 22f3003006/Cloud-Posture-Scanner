import React, { useEffect } from 'react'
import axios from 'axios'
import { useState } from 'react'
import './EC2.css'
function EC2() {
  const [inst, setInst] = React.useState([])
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/instances')
      .then(response => {
        setInst(response.data)
      })
  }, [])

  return (
    <div className='box'>
        <h2>EC2 Instances</h2>
        {inst.length === 0 ? (
            <p style={{ fontStyle: 'italic', textAlign: 'center', marginTop: '2rem'}}>Loading, Please Wait....</p>
        ) : (
            <table border="1">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Region</th>
                    <th>Public IP</th>
                    <th>Security Groups</th>
                </tr>
                </thead>
                <tbody>
                {inst.map(i => (
                    <tr key={i.InstanceId}>
                        <td>{i.InstanceId}</td>
                        <td>{i.InstanceType}</td>
                        <td>{i.Region}</td>
                        <td>{i.PublicIpAddress || "N/A"}</td>
                        <td>
                        {i.SecurityGroups && i.SecurityGroups.length > 0
                            ? i.SecurityGroups.map(sg => sg.GroupName).join(", ")
                            : "N/A"}
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        )}
    </div>
  )
}

export default EC2