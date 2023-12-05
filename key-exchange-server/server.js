const mongoose = require('mongoose');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors')

mongoose.connect('mongodb+srv://at822076:balls123@iot.os0xjzn.mongodb.net/?retryWrites=true&w=majority')
console.log('Connected to MongoDB')

const app = express();
const port = 3001;

const userSchema = new mongoose.Schema({
    userId: String,
    passwordHash: String,
    key : String,
});

const User = mongoose.model('User', userSchema);

app.use(cors());
app.use(bodyParser.json());

app.post('/authenticate', async (req, res) => {
  console.log(req.body)
    var { userId, passwordHash, key } = req.body;
    try {
        var user = await User.findOne({ userId });

        if (!user) {
            user = new User({
                userId,
                passwordHash: passwordHash,
                key,
              });
        
              await user.save();
              return res.json({key : 2})
        }

        if (passwordHash != user.passwordHash) {
            return res.json({ key: 0 });
        }

        return res.json({ key: 1 });
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});


app.get('/get-key/:userId', async (req, res) => {
    const { userId } = req.params;
  
    try {
      const user = await User.findOne({ userId });

      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
  
      return res.json({ key: user.key });
    } catch (error) {
      console.error(error);
      res.status(500).send('Internal Server Error');
    }
  });

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
