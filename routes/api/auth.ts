import User from "../../models/User";

import express, {Request, Response, Application, Router} from 'express';

import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';


const router: Router = express.Router();


router.post('/', async (req: Request, res: Response) => {
    
    const { email, password } = req.body;

    try {
        // if user exists
        let user = await User.findOne(({ email }));
        if(!user){
            return res.status(400).json({ errors: [ { msg: 'Invalid Credentials.' } ] })
        }

        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch){
            return res.status(400).json({ errors: [ { msg: 'Invalid Credentials.' } ] })
        }

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

    }
    catch(err: any){
        console.error(err.message);
        res.status(500).send('Server error.');
    }

})


export default router;