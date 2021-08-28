import { Schema, model, createConnection } from 'mongoose';


const db: any = process.env.mongoPublicURI;


export default async () => {
    try {
        const conn: any = await createConnection(db, {});
        console.log(`Ciao, MongoDB connected... `);
        console.log(conn.client.options.srvHost)
    } catch(err: any){
        console.error(err.message);
        process.exit(1);
    }
}