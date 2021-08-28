import User from "../../models/User";

import express, {Request, Response, Application, Router} from 'express';
import gravatar from 'gravatar';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const router: Router = express.Router();


router.post('/', async (req: Request, res: Response) => {
    

    try {
        
        const { name, email, password } = req.body;

        let user: any = await User.findOne(({ email }))

        if (user) {
            return res.status(400).json({ errors: [ { msg: 'User already exists.' } ] })
        }

        const avatar = gravatar.url(email, {
            s: '200', r: 'pg', d: 'mm'
        //  size, rating, default image
        });


        user = new User({
            name,
            email,
            avatar,
            password
        });

        // encrypt password using bcrypt
        const salt = await bcrypt.genSalt(10);

        user.password = await bcrypt.hash(password, salt);

        await user.save();

        const payload = {
            user: {
                id: user.id
            }
        }
        const JWTSecretKey: any = process.env["jwtSecret"]
        jwt.sign(payload, JWTSecretKey, { expiresIn: 360000 },
        (err, token) => {
            if(err) {
                throw err
            }
            res.json({ token }); 
                
        });
        

    } catch(err: any){
        console.error(err.message);
        res.status(500).send('Server error.');
    }

})


export default router;