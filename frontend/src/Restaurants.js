import React, { Component } from 'react'
import DistChart from './DistChart'
import Restaurant from './Restaurant'
import ResetButton from './ResetButton'
import RecommendationButton from './RecommendationButton'
import RecommendationInfo from './RecommendationInfo'
import ColorHash from 'color-hash'

export default class Restaurants extends Component {
    constructor(props) {
        super(props)
        this.state = {
            distributions: [],
            recommendation: null,
        }
    }

    colorHash = new ColorHash()

    updateDistributions = () => fetch('/api/restaurants')
        .then((result) => result.json())
        .then(({ distributions }) => {
            distributions = distributions.map((d) => Object.assign({}, d, {
                restaurant: Object.assign({}, d.restaurant, {
                    color: this.colorHash.hex(d.restaurant.id)
                })
            }))
            this.setState({
                distributions,
            })
        })

    getRecommendation = () => fetch('/api/sample')
        .then((result) => result.json())
        .then((recommendation) => 
            this.setState({ recommendation }))

    componentDidMount = this.updateDistributions

    render() {
        const { distributions, recommendation } = this.state

        return (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: '40px' }}>
                <div style={{ float: 'left' }}>
                    <DistChart
                        distributions={this.state.distributions}
                        sampledProbabilities={recommendation && recommendation.probabilities}
                        height="500px"
                        width="1000px"
                    />
                </div>
                <div style={{ float: 'left', marginLeft: '20px' }}>
                    <div style={{ marginBottom: '40px' }}>
                        {recommendation && <RecommendationInfo
                            restaurant={recommendation.restaurant}
                        />}
                        <RecommendationButton onClick={this.getRecommendation} />
                    </div>
                    <div style={{ marginBottom: '40px' }} >
                        {distributions.map((d) =>
                            <Restaurant
                                key={d.restaurant.id}
                                restaurant={d.restaurant}
                                onUpdate={this.updateDistributions}
                            />
                        )}
                    </div>
                    <ResetButton onClick={this.updateDistributions} />
                </div>
            </div>
        )
    }
}