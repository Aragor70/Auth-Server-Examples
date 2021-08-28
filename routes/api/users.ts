import User from "../../models/User";

import express, {Request, Response, Application, Router} from 'express';


const router: Router = express.Router();


router.post('/', async (req: Request, res: Response) => {
    
    const { email, password } = req.body;

    try {

        console.log(email)

        res.json(req.body)

    } catch(err: any){
        console.error(err.message);
        res.status(500).send('Server error.');
    }

})


export default router;