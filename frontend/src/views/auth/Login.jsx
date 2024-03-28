import React, {useState, useEffect} from 'react'
import  { login } from '../../utils/auth'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../store/auth'


function Login() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [isLoading, setIsLoading] = useState(false)

    const isLoggedIn = useAuthStore((state) => state.isLoggedIn)

    const navigate = useNavigate()

    console.log(email);
    console.log(password);
    useEffect(() => {
        if(isLoggedIn()){
            navigate('/')
        }
    }, [])
    
    const resetForm = () => {
        setPassword("")
        setEmail("")
    }

    const handleLogin = async (e) => {
        e.preventDefault()
        setIsLoading(true)

        const {error} = await login(email, password)
        if (error) {
            alert(error)
            setIsLoading(false)
        } else {
            navigate('/')
            resetForm()
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
                      <h3 className="text-center">Login to Riz Avenue</h3>
                      <br />

                      <div className="tab-content">
                        <div
                          className="tab-pane fade show active"
                          id="pills-login"
                          role="tabpanel"
                          aria-labelledby="tab-login"
                        >
                          <form onSubmit={handleLogin}>
                            {/* Email input */}
                            <div className="form-outline mb-4">
                              <label className="form-label" htmlFor="loginName">
                                Email Address
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

                            <div className="form-outline mb-4">
                              <label
                                className="form-label"
                                htmlFor="loginPassword"
                              >
                                Password
                              </label>
                              <input
                                type="password"
                                id="loginpassword"
                                required
                                name="password"
                                value={password}
                                className="form-control"
                                onChange={(e) => setPassword(e.target.value)}
                              />
                            </div>

                            {isLoading === true ? (
                              <button
                                disabled
                                className="btn btn-primary w-100"
                                type="submit"
                                //   disabled={"isLoading"}
                              >
                                <span className="mr-2">Logging in... </span>
                                <i className="fas fa-spinner fa-spin" />
                              </button>
                            ) : (
                              <button
                                className="btn btn-primary w-100"
                                type="submit"
                                //   disabled={"isLoading"}
                              >
                                <span className="mr-2">Login </span>
                                <i className="fas fa-sign-in" />
                              </button>
                            )}

                            <div className="text-center">
                              <p className="mt-4">
                                New to Riz Avenue?{" "}
                                <Link to="/register">Register</Link>
                              </p>
                              <p className="mt-0">
                                <Link
                                  to="/forgot-password/"
                                  className="text-danger"
                                >
                                  Forgot Password?
                                </Link>
                              </p>
                            </div>
                          </form>
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

export default Login