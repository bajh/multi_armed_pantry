import React, { Component } from 'react'

export default class RecommendationButton extends Component {
    render() {
        return (
            <button onClick={this.props.onClick} style={{borderStyle: 'solid'}}>
                Get Recommendation
            </button>
        )
    }
}