import React, { Component } from 'react';

import {creatData} from '../utils';



const IP = '172.20.10.2';
const PORT = 3000
const API = 'api/rpi/data/'

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pointer: 0,
            time: 500,
            numOfRow: 16,
            numOfCol: 16,
            data: creatData(16, 16)
        };
    }
    componentWillMount() {
        const {time, numOfRow, data} = this.state;
        this.triggerInterval =
            setInterval(() => {
                this.sendData(data[this.state.pointer]);
                this.setState({
                    pointer: (this.state.pointer+1) % numOfRow
                })
        }, time);
               
    }
    async sendData(data) {
        const url = `http://${IP}:${PORT}/${API}`
        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({data}),
                mode: 'no-cors' ,
            });
        } catch(e){

        }
    }
    componentWillUnmount() {
        clearInterval(this.triggerInterval);
    }
    render() {
        const {data, pointer} = this.state;
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

const Col = ({data, c_idx, pointer, onClick}) => {
    const isHit = pointer === c_idx;
    return (
        <div className = {`col ${isHit? 'hit':''}`}>
            {
                data.map((flag, i)=>
                    <Row
                        key = {i} 
                        c_idx = {c_idx}
                        r_idx = {i}
                        pointer = {pointer}
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
            className={`row ${flag? 'Red':'Light-Gray'}`}
            onClick = {
                ()=>
                    onClick(c_idx, r_idx)}
        >
        </div>
    )
}