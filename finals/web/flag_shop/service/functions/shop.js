// format functions
const inventory = require('./menu');
const Shop = module.exports;
const cart = [];

Shop.add = (_, item) => {
    cart.push(item);
    return cart;
}

Shop.removeByIndex = (_, index) => {
    cart.pop(item);
    return cart;
}

Shop.list = (_, __) => {
    return inventory.items;
}