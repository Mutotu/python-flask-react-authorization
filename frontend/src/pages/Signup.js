import { useState } from "react";
import axios from "axios";

const Signup = (props) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/users`, {
        email,
        password,
      })
      .then((response) => {
        props.setUser(response.data.user);
        // localStorage.setItem("userId", response.data.user.id);
        localStorage.setItem("userId", response.data.user_id);
      })
      .catch((err) => {
        setError(err.response.data.message);
        // console.log(err);
      });
  };

  return (
    <div>
      <h2>Sign up for an accout!</h2>

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
          <input type='submit' value='Sign up!'></input>
        </div>
      </form>
    </div>
  );
};

export default Signup;
