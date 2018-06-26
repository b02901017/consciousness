import React, { Component } from "react";

import {creatData} from "../utils";



const IP = "172.20.10.2";
const PORT = 3000
const API = "api/rpi/data/"


const key2idx = {
    "1":0,
    "2":1,
    "3":2,
    "q":6,
    "w":7,
    "e":8,
    "a":12,
    "s":13,
    "d":14,
    "z":18,
    "x":19,
    "c":20,
    "0":3,
    "-":4,
    "=":5,
    "o":9,
    "p":10,
    "[":11,
    "k":15,
    "l":16,
    ";":17,
    "m":21,    
    ",":22,    
    ".":23,    
}
class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pointer: 0,
            beat : false,
            time: 200,
            numOfRow: 4,
            numOfCol: 4,
            data: creatData(6, 4),
            isSend: false
        };
    }
    componentWillMount() {
        const {time, numOfRow, data} = this.state;
        this.triggerInterval =
            setInterval(() => {
                if (this.state.beat && this.state.isSend) {
                    this.sendData(data);
                }
                this.setState({
                    // pointer: (this.state.pointer+1) % numOfRow,
                    beat: !this.state.beat
                })
        }, time);
        document.addEventListener("keydown", this._handleKeyDown.bind(this));
    }
    async sendData(data) {
        data = [].concat.apply([], data);
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
        let i = idx % 6;
        let j = parseInt(idx / 6);
        let _data = [...data]; 
        _data[i][j] =  _data[i][j] ? 0 :1;
        this.setState({
            data: _data
        })
    }
    render() {
        const {data, pointer, beat, isSend} = this.state;
        return (
            <div className="container"> 
                <div className = 'btn-row'>
                    <div
                        onClick = {()=>{
                            this.sendData(creatData(6, 4))
                            this.setState({isSend: !isSend})}}
                        className = {`btn ${isSend ? 'Green': 'Light-Gray'}`}>
                    </div>
                </div>
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
