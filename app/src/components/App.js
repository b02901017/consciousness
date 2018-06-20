import React, { Component } from "react";

import {creatData} from "../utils";



const IP = "172.20.10.2";
const PORT = 3000
const API = "api/rpi/data/"


const key2idx = {
    "q":0,
    "w":1,
    "e":2,
    "r":3,
    "a":8,
    "s":9,
    "d":10,
    "f":11,
    "z":16,
    "x":17,
    "c":18,
    "v":19,
    "o":4,
    "p":5,
    "[":6,
    "]":7,
    "k":12,
    "l":13,
    ";":14,
    "'":15,
    "m":20,
    ",":21,    
    ".":22,    
    "/":23,    
}
class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pointer: 0,
            beat : false,
            time: 500,
            numOfRow: 4,
            numOfCol: 4,
            data: creatData(8, 3)
        };
    }
    componentWillMount() {
        const {time, numOfRow, data} = this.state;
        this.triggerInterval =
            setInterval(() => {
                this.sendData(data[this.state.pointer]);
                this.setState({
                    pointer: (this.state.pointer+1) % numOfRow,
                    beat: !this.state.beat
                })
        }, time);
        document.addEventListener("keydown", this._handleKeyDown.bind(this));
    }
    async sendData(data) {
        const url = `http://${IP}:${PORT}/${API}`
        try {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({data}),
                mode: "no-cors" ,
            });
        } catch(e){
        }
    }
    componentWillUnmount() {
        clearInterval(this.triggerInterval);
        document.removeEventListener("keydown", this._handleKeyDown.bind(this));
    }
    _handleKeyDown({key}){
        const {data, pointer, beat} = this.state;
        const idx = key2idx[key];
        if (idx === undefined) 
            return;
        let i = idx % 8;
        let j = parseInt(idx / 8);
        let _data = [...data]; 
        _data[i][j] =  _data[i][j] ? 0 :1;
        this.setState({
            data: _data
        })
    }
    render() {
        const {data, pointer, beat} = this.state;
        return (
            <div className="container"> 
                <div className="pad Gray"> 
                    {
                        data.map((obj, i)=>
                            <Col
                                key = {i} 
                                c_idx = {i}
                                data = {obj}
                                pointer = {pointer}
                                beat = {beat}
                                onClick = {
                                    (i, j)=>{
                                        let _data = [...data]; 
                                        _data[i][j] =  _data[i][j] ? 0 :1;
                                        this.setState({
                                            data: _data
                                        })
                                    }
                                }
                            />
                        )
                    }
                </div>
            </div>
    );
  }
}

export default App;

const Col = ({data, c_idx, pointer, onClick, beat}) => {
    // const isHit = pointer === c_idx;
    const isHit = beat;
    return (
        <div className = {`col ${isHit? "hit":""}`}>
            {
                data.map((flag, i)=>
                    <Row
                        key = {i} 
                        c_idx = {c_idx}
                        r_idx = {i}
                        flag = {flag}
                        onClick = {onClick}/>
                )
            }
        </div>
    )
}
const Row = ({onClick, c_idx, r_idx, flag}) => {
    return (
        <div
            className={`row ${flag? "Red":"Light-Gray"}`}
            onClick = {
                ()=>
                    onClick(c_idx, r_idx)}
        >
        </div>
    )
}