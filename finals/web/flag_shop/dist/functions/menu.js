const menu = module.exports;
menu.items = {
    'egg fried rice': 10, 
    'chang': 20,
    'singha': 20, 
    'butter cack': 5,
    'green curry': 7,
    'tom yum': 8,
}

menu.add = (sess, item) => {
    // TODO add functionality to add items to the menu
    return menu.items;
}

menu.remove = (sess, item) => {
    if (!sess.admin) return menu.items;
    delete menu.items[item];
    return menu.items;
}
