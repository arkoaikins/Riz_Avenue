import { useState } from 'react'
import creatAPIInstance from '../../utils/axios';
import { useNavigate, Link } from "react-router-dom";

function ForgotPassword() {
    const [email, setEmail] = useState("")
    const [isLoading, setIsLoading] = useState(false);

    const navigate =  useNavigate()
    

    const handleReset = async () => {
        setIsLoading(true);
        try {
            await creatAPIInstance.get(`user/password-reset/${email}/`).then((res) =>{
                alert("An Email has been sent to you.")
                setIsLoading(false);
            })

        } catch (error) {
            alert("NO account associated with this Email")
            setIsLoading(false);
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
                      <h3 className="text-center">Riz Avenue Password Reset</h3>
                      <br />
                      <div>
                        {/* Email input */}
                        <div className="form-outline mb-4">
                          <label className="form-label" htmlFor="loginName">
                            Email
                          </label>
                          <input
                            type="email"
                            id="loginName"
                            required
                            name="email"
                            value={email}
                            className="form-control"
                            onChange={(e) => setEmail(e.target.value)}
                          />
                        </div>

                        {isLoading === true ? (
                          <button
                            disabled
                            className="btn btn-primary w-100"
                            type="button"
                          >
                            <span className="mr-2">Sending Email... </span>
                            <i className="fas fa-spinner fa-spin" />
                          </button>
                        ) : (
                          <button
                            onClick={handleReset}
                            className="btn btn-primary w-100"
                            type="button"
                          >
                            <span className="mr-2">Send Email </span>
                            <i className="fas fa-paper-plane" />
                          </button>
                        )}

                        <div className="text-center">
                          <p className="mt-4">
                            Login to Riz Avenue? <Link to="/login">Login</Link>
                          </p>
                        </div>
                      </div>
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

export default ForgotPassword