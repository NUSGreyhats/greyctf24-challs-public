// format functions

const user = module.exports;

user.checkout = (sess, _) => {
    for (const item of sess.order) {
        if (item === "flag"){
            return process.env.FLAG;
        }
    }
    sess.order = [];
    return 'ok';
}