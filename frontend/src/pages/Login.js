import { useState } from "react";
import axios from "axios";

const Login = (props) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const response = await axios.post(
      // `${process.env.REACT_APP_BACKEND_URL}/users/login`,
      "http://localhost:5000/users/login",
      {
        email,
        password,
      }
    );

    // .then((response) => {
    props.setUser(response.data.user);
    // localStorage.setItem("userId", response.data.user_id);
    localStorage.setItem("userId", response.data.User_id);
    // console.log(response);
    // })
    // .catch((err) => {
    // setError(err.response.data.message);
    // console.log(err);
    // });
  };

  return (
    <div>
      <h2>Log into your accout!</h2>

      {error && <div className='error'>{error}</div>}

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor='signup-email'>Email:</label>
          <input
            id='signup-email'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor='signup-password'>Password:</label>
          <input
            id='signup-password'
            type='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <input type='submit' value='Log in!'></input>
        </div>
      </form>
    </div>
  );
};

export default Login;
