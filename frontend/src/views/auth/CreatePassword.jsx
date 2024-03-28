import {useState} from 'react'
import { useSearchParams, useNavigate, Link } from 'react-router-dom'
import creatAPIInstance from '../../utils/axios'


function CreatePassword() {
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [isLoading, setIsLoading] = useState(false);
    
    const navigate = useNavigate()
    
    const [searchParam] = useSearchParams()
    const otp = searchParam.get("otp")
    const uidb64 = searchParam.get("uidb64")
    
    const handlePasswordSubmit = async (e) => {
        setIsLoading(true);
        e.preventDefault()
        
        if(password !== confirmPassword){
            alert("Password Do Not Match")
            setIsLoading(false);
        } else {
            setIsLoading(true);
            const formdata = new FormData()
            formdata.append('password', password)
            formdata.append('otp', otp)
            formdata.append('uidb64', uidb64)

            try {
                await creatAPIInstance.post(`user/password-change/`, formdata).then((res) => {
                    console.log(res.data);
                    alert("Password Change Successfully")
                    navigate("/login")
                    setIsLoading(false);

                })
            } catch (error) {
                console.error(error); 
                alert("An error occured while trying to change the password")
                setIsLoading(false);
            }

        }
    }
   
    return (
      <>
        <main className="" style={{ marginBottom: 100, marginTop: 50 }}>
          <div className="container">
            {/* Section: Login form */}
            <section className="">
              <div className="row d-flex justify-content-center">
                <div className="col-xl-5 col-md-8">
                  <div className="card rounded-5">
                    <div className="card-body p-4">
                      <h3 className="text-center">
                        Create a New Riz Avenue Password
                      </h3>
                      <br />
                      <form onSubmit={handlePasswordSubmit}>
                        {/* Email input */}
                        <div className="form-outline mb-4">
                          <label className="form-label" htmlFor="loginName">
                            New Password
                          </label>
                          <input
                            type="password"
                            id="loginName"
                            required
                            name="password"
                            value={password}
                            className="form-control"
                            onChange={(e) => setPassword(e.target.value)}
                          />
                        </div>
                        <div className="form-outline mb-4">
                          <label className="form-label" htmlFor="loginName">
                            Confirm Password
                          </label>
                          <input
                            type="password"
                            required
                            name="password"
                            value={confirmPassword}
                            className="form-control"
                            onChange={(e) => setConfirmPassword(e.target.value)}
                          />
                        </div>

                        {isLoading === true ? (
                          <button
                            disabled
                            className="btn btn-primary w-100"
                            type="button"
                          >
                            <span className="mr-2">Changing Password </span>
                            <i className="fas fa-spinner fa-spin" />
                          </button>
                        ) : (
                          <button
                            className="btn btn-primary w-100"
                            type="submit"
                          >
                            <span className="mr-2">Save Password </span>
                            <i className="fas fa-check-circle" />
                          </button>
                        )}

                        <div className="text-center">
                          <p className="mt-4">
                            Login to Riz Avenue? <Link to="/login">Login</Link>
                          </p>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </main>
      </>
    );
}

export default CreatePassword