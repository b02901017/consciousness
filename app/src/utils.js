export function creatData(row, col) {
    let arr = new Array(row);
    for (let i = 0; i < row; i++) {
        arr[i] = Array.apply(null, Array(col)).map(Number.prototype.valueOf, 0);
    }
    return arr;
}