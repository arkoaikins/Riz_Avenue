import React, {useState, useEffect} from 'react'
import  { register } from '../../utils/auth'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../store/auth'



function Register() {
    const [fullname, setFullname] = useState("")
    const [email, setEmail] = useState("")
    const [mobile, setMobile] = useState("")
    const [password, setPassword] = useState("")
    const [password2, setPassword2] = useState("")

    const [isLoading, setIsLoading] = useState(false)

    const isLoggedIn = useAuthStore((state) => state.isLoggedIn)

    const navigate = useNavigate()

    useEffect(() => {
        if(isLoggedIn()){
            navigate("/")
        }
    }, [isLoading])

    const handleSubmit = async (e) => {
        e.preventDefault()
        setIsLoading(true)

        const {error} = await register( fullname, email, mobile, password, password2)
        if (error) {
            alert(JSON.stringify(error))
        } else {
            navigate("/")
        }
    }
    return (
        <div>
            <div>Register</div>
            <form onSubmit={handleSubmit}>
                <input 
                type="text" 
                placeholder='Full Name' 
                name="" 
                id=""
                onChange={(e) => setFullname(e.target.value)}
                />
                <br />
                <br />
            
                <input 
                type="email" 
                placeholder='Email' 
                name="" 
                id=""
                onChange={(e) => setEmail(e.target.value)}
                />
                <br />
                <br />
                
                <input 
                type="number" 
                placeholder='Phone' 
                name="" 
                id="" 
                onChange={(e) => setMobile(e.target.value)}
                />
                <br />
                <br />
                
                <input 
                type="password" 
                placeholder='Enter Password' 
                name="" 
                id=""
                onChange={(e) => setPassword(e.target.value)}
                />
                <br />
                <br />
                
                <input 
                type="password" 
                placeholder='Confirm Password' 
                name="" 
                id=""
                onChange={(e) => setPassword2(e.target.value)}
                />
                <br />
                <br />
                <button type='submit'>Register</button>

            </form>
        </div>
    )
}

export default Register