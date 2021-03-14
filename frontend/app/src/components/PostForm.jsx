import React, { Component } from 'react';
import axios from 'axios'

class PostForm extends Component {
    constructor(props) {
        super(props)
        this.state = {
            From:'',
            To:'',
            Amt:''
        }
    }

    myChangeHandler = (e) => {
        this.setState({[e.target.name]:e.target.value})
    }

    submitHandler = (e) => {
        e.preventDefault()
        axios.post('/receive_transactions', this.state)
    }

    render() { 
 
        const {From,To,Amt} = this.state;

        return ( 
        <div>
            <form onClick={this.submitHandler}>
                <input type="text" name='From' value={this.From} onChange={this.myChangeHandler}/>
                <input type="text" name='To' value={this.To} onChange={this.myChangeHandler}/>
                <input type="text" name='Amt' value={this.Amt} onChange={this.myChangeHandler}/>
                <button type='submit'>Submit</button>
            </form>
        </div>
         );
    }
}
 
export default PostForm;