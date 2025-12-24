import React from 'react'
import axios from 'axios'
import { useState, useEffect } from 'react'
function Results() {
  const [res,setRes]=useState([]);
  useEffect(()=>{
    axios.get("http://127.0.0.1:8000/cis-results")
    .then((response)=>{
      setRes(response.data);
    })
  },[]);

  return (
    <div className='res-box'>
        <h2>CIS Results</h2>
        {res.length===0 ? (
            <p style={{ fontStyle: 'italic', textAlign: 'center', marginTop: '2rem'}}>Loading, Please Wait....</p>
        ) :
            <table border="1">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>Evidence</th>
                </tr>
                </thead>
                <tbody>
                {res.map((r, idx) => (
                    <tr key={idx}>
                    <td>{r["CIS ID"]}</td>
                    <td>{r.Description}</td>
                    <td>{r.Status}</td>
                    <td>{r.Evidence==[] || r.Evidence==0 ? "N/A" : r.Evidence.map(e=>e.GroupId).join(", ")}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        }
    </div>
  )
}

export default Results