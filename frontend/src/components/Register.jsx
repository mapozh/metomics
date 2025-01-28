import React, { useState, useEffect } from 'react';
import '../styles/Register.css';
import { useNavigate } from 'react-router-dom';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import axios from 'axios';

const Register = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    initial: '',
    firstName: '',
    lastName: '',
    position: '',
    labName: '',
    email: '',
    confirmEmail: '',
    password: '',
    confirmPassword: '',
    terms: false,
    passwordValidation: {
      length: false,
      capital: false,
      number: false,
      special: false,
      match: false,
    },
    validation: {
      emailMatch: true,
      emailValid: true,
      passwordMatch: true,
      isPasswordValid: true,
      termsAccepted: true,
    },
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false); // Button loading state
  const [errorMessage, setErrorMessage] = useState(''); // Display error messages

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  // Validate password strength
  const checkPasswordValidation = (password, confirmPassword) => {
    setForm(prevState => ({
      ...prevState,
      passwordValidation: {
        length: password.length >= 8,
        capital: /[A-Z]/.test(password),
        number: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
        match: password === confirmPassword,
      },
      validation: {
        ...prevState.validation,
        passwordMatch: password === confirmPassword,
        isPasswordValid: password.length >= 8 && /[A-Z]/.test(password) && /\d/.test(password) && /[!@#$%^&*(),.?":{}|<>]/.test(password),
      }
    }));
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    const updatedForm = {
      ...form,
      [name]: type === 'checkbox' ? checked : value,
    };
    setForm(updatedForm);

    // Update password validation
    if (name === 'password' || name === 'confirmPassword') {
      checkPasswordValidation(updatedForm.password, updatedForm.confirmPassword);
    }

    // Update email and other validation checks
    setForm(prevState => ({
      ...prevState,
      validation: {
        emailMatch: updatedForm.email === updatedForm.confirmEmail,
        emailValid: /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/.test(updatedForm.email),
        passwordMatch: updatedForm.password === updatedForm.confirmPassword,
        isPasswordValid: prevState.passwordValidation.length && prevState.passwordValidation.capital && prevState.passwordValidation.number && prevState.passwordValidation.special,
        termsAccepted: updatedForm.terms,
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const { validation, passwordMatch, isPasswordValid } = form;

    // Ensure form validation checks
    if (!validation || !validation.emailMatch || !validation.emailValid || !passwordMatch || !isPasswordValid || !form.terms) {
      setErrorMessage('Please fill out all required fields correctly.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    // Log the data that will be sent to the backend
    console.log('Sending registration data to the backend:', {
      initial: form.initial,
      first_name: form.firstName,
      last_name: form.lastName,
      position: form.position,
      lab_name: form.labName,
      email: form.email,
      password: form.password,
      confirm_password: form.confirmPassword,
    });
    
    try {
      const response = await axios.post('http://localhost:5000/register', {
        initial: form.initial,
        first_name: form.firstName,
        last_name: form.lastName,
        position: form.position,
        lab_name: form.labName,
        email: form.email,
        password: form.password,
        confirm_password: form.confirmPassword,
      });

      if (response.data.message) {
        navigate('/authorization');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      if (error.response && error.response.data && error.response.data.detail) {
        const errorDetail = Array.isArray(error.response.data.detail)
          ? error.response.data.detail.map((err) => err.msg).join(', ')
          : error.response.data.detail;

        setErrorMessage(errorDetail);
      } else {
        setErrorMessage('An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => setShowPassword(!showPassword);
  const toggleConfirmPasswordVisibility = () => setShowConfirmPassword(!showConfirmPassword);

  const isFormValid = form.validation.emailMatch && form.validation.emailValid && form.validation.passwordMatch && form.validation.isPasswordValid && form.validation.termsAccepted;

  return (
    <div className="register-container">
      <h1 className="page-title">OMIXS</h1>
      <h4 className="page-description">
        Unlock the power of automated omics data management with OMIX. Seamlessly integrate, query, and store complex datasets with our cutting-edge platform, designed to eliminate manual data handling, streamline workflows, and enhance research efficiency—all while ensuring data accuracy and security.
      </h4>
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register</h2>

        {/* Error Message */}
        {errorMessage && <div className="error-message">{errorMessage}</div>}

        {/* Form Fields */}
        <div className="form-group">
          <select name="initial" value={form.initial} onChange={handleChange} className="form-control">
            <option value="">Select Initial</option>
            <option value="Dr.">Dr.</option>
            <option value="Mr.">Mr.</option>
            <option value="Mrs.">Mrs.</option>
            <option value="Ms.">Ms.</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <input type="text" name="firstName" placeholder="First Name" value={form.firstName} onChange={handleChange} className="form-control" />
        </div>

        <div className="form-group">
          <input type="text" name="lastName" placeholder="Last Name" value={form.lastName} onChange={handleChange} className="form-control" />
        </div>

        <div className="form-group">
          <select name="position" value={form.position} onChange={handleChange} className="form-control">
            <option value="">Select Role in Lab</option>
            <option value="Lab Technician">Lab Technician</option>
            <option value="Pathologist">Pathologist</option>
            <option value="Pathologist Assistant">Pathologist Assistant</option>
            <option value="Administrator">Administrator</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <input type="text" name="labName" placeholder="Lab Name" value={form.labName} onChange={handleChange} className="form-control" />
        </div>

        <div className="form-group">
          <input type="email" name="email" placeholder="Email" value={form.email} onChange={handleChange} className="form-control" />
          {!form.validation.emailValid && <small className="error">Please enter a valid email</small>}
        </div>

        <div className="form-group">
          <input type="email" name="confirmEmail" placeholder="Confirm Email" value={form.confirmEmail} onChange={handleChange} className="form-control" />
          {!form.validation.emailMatch && <small className="error">Emails do not match</small>}
        </div>

        <div className="form-group" style={{ position: 'relative' }}>
          <input type={showPassword ? 'text' : 'password'} name="password" placeholder="Password" value={form.password} onChange={handleChange} className="form-control" />
          <span onClick={togglePasswordVisibility} style={{ cursor: 'pointer', position: 'absolute', right: '10px', top: '10px', zIndex: 1 }}>
            {showPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
          </span>
        </div>

        <div className="form-group">
          <input type={showConfirmPassword ? 'text' : 'password'} name="confirmPassword" placeholder="Confirm Password" value={form.confirmPassword} onChange={handleChange} className="form-control" />
          <button type="button" onClick={toggleConfirmPasswordVisibility} className="eye-icon">
            {showConfirmPassword ? <VisibilityOffIcon /> : <VisibilityIcon />}
          </button>
          {!form.validation.passwordMatch && <small className="error">Passwords do not match</small>}
        </div>

        <div className="password-validation">
          <ul>
            <li className={form.passwordValidation.length ? 'valid' : ''}>Password must be at least 8 characters</li>
            <li className={form.passwordValidation.capital ? 'valid' : ''}>Password must include at least one capital letter</li>
            <li className={form.passwordValidation.number ? 'valid' : ''}>Password must include at least one number</li>
            <li className={form.passwordValidation.special ? 'valid' : ''}>Password must include at least one special character</li>
            <li className={form.passwordValidation.match ? 'valid' : ''}>Passwords must match</li>
          </ul>
        </div>

        <div className="form-group">
          <label>
            <input type="checkbox" name="terms" checked={form.terms} onChange={handleChange} />
            I agree to the <a href="/terms-of-service" target="_blank">Terms & Conditions</a>
          </label>
          {!form.validation.termsAccepted && <small className="error">You must accept the Terms & Conditions</small>}
        </div>

        <button type="submit" disabled={!isFormValid || loading} style={{ backgroundColor: isFormValid ? 'green' : 'grey', cursor: isFormValid ? 'pointer' : 'not-allowed' }}>
          {loading ? 'Registering...' : 'Register'}
        </button>

        <p>
          Already have an account? <span onClick={() => navigate('/signin')} style={{ color: 'blue', cursor: 'pointer' }}>Sign In</span>
        </p>
      </form>
    </div>
  );
};

export default Register;



// components/Register.jsx

// import React from 'react';

// const Register = () => {
//   return <div>Register Page</div>;
// };

// export default Register;
