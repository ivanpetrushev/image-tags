function lm(str){
    try {
        console.log(str);
    }
    catch (e){
        // do nothing
    }
}

function getVal(name, defaultValue) {
    try {
        return eval(name);
    }
    catch (e) {
        return defaultValue;
    }
}


