import React, { Component } from "react";

import {creatData} from "../utils";



const IP = "172.20.10.2";
const PORT = 3000
const API = "api/rpi/data/"


const key2idx = {
    "1":0,
    "q":1,
    "a":2,
    "z":3,
    "2":4,
    "w":5,
    "s":6,
    "x":7,
    "3":8,
    "e":9,
    "d":10,
    "c":11,
    "4":12,
    "r":13,
    "f":14,
    "v":15,
    "5":16,
    "t":17,
    "g":18,
    "b":19,
    "6":20,
    "y":21,    
    "h":22,    
    "n":23,    
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
            data: creatData(6, 4)
        };
    }
    componentWillMount() {
        const {time, numOfRow, data} = this.state;
        this.triggerInterval =
            setInterval(() => {
                this.sendData(data);
                this.setState({
                    pointer: (this.state.pointer+1) % numOfRow,
                    beat: !this.state.beat
                })
        }, time);
        document.addEventListener("keydown", this._handleKeyDown.bind(this));
    }
    async sendData(data) {
        const url = `http://${IP}:${PORT}/${API}`
        data  = [].concat.apply([], data);
        console.log(data)
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
        let i = idx % 4;
        let j = parseInt(idx / 4);
        let _data = [...data]; 
        _data[j][i] =  _data[j][i] ? 0 :1;
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