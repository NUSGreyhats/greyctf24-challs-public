// format functions
const order = module.exports;
const menu = require('./menu');
order.add = (sess, item) => {
    if (Object.keys(menu.items).includes(item)) {
        sess.order.push(item);; 
    }
    return sess.order;
}

order.removeByIndex = (sess, index) => {
    sess.order.splice(index, 1);
    return true;
}

order.view = (sess, _) => {
    return sess.order;
}
