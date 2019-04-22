import React, { Component } from 'react'

export default class ResetButton extends Component {
    handleClick = () => fetch('/api/reset', { method: 'POST' })
        .then(() => this.props.onClick())

    render() {
        return (
            <button onClick={this.handleClick} style={{borderStyle: 'solid'}}>
                Reset
            </button>
        )
    }
}