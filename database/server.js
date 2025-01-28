const { Pool } = require('pg');
require('dotenv').config();

// Create a new Pool instance
const pool = new Pool({
  user: 'postgres',     // Database user
  host: 'localhost',        // Host where PostgreSQL is running
  database: 'postgres', // Your database name
  password: 'RiscaniM',// Your database password
  port: 5432,               // Default PostgreSQL port
});



// POST endpoint to handle registration
app.post('/register', async (req, res) => {
    const { initial, first_name, last_name, position, lab_name, email, password, confirm_password } = req.body;
  
    if (password !== confirm_password) {
      return res.status(400).send({ message: 'Passwords do not match' });
    }
  
    try {
      const result = await pool.query(
        `INSERT INTO users (initial, first_name, last_name, position, lab_name, email, password)
         VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
        [initial, first_name, last_name, position, lab_name, email, password]
      );
  
      res.status(201).send({ message: 'Registration successful', user: result.rows[0] });
    } catch (err) {
      console.error('Error during registration:', err.stack);
      res.status(500).send({ message: 'Server error, please try again later.' });
    }
  });
  
  const port = process.env.PORT || 5000;
  app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
  
