import { useState } from 'react'
import creatAPIInstance from '../../utils/axios';
import { useNavigate } from 'react-router-dom';

function ForgotPassword() {
    const [email, setEmail] = useState("")

    const navigate =  useNavigate()
    

    const handleReset = async () => {
        try {
            await creatAPIInstance.get(`user/password-reset/${email}/`).then((res) =>{
                alert("An Email has been sent to you.")
            })

        } catch (error) {
            alert("NO account associated with this Email")
        }
                        
    }

    return (
        <div>
            <h1>ForgotPassword</h1>
            <input 
            onChange={(e) => setEmail(e.target.value)}
            type="email" 
            placeholder='Enter your Email' 
            name=""
            id="" 
            />
            <br />
            <br />
            <button onClick={handleReset}>Reset Password</button>


        </div>
    )
}

export default ForgotPassword