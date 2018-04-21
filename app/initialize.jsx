import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import _ from 'lodash'


class Search extends Component {

  constructor(props) {
    super(props)
    this.state = {
      keywords: [],
      results: []
    }
  }

  handleSearch(e) {
    e.preventDefault()

    const value = e.target.query.value
    const { keywords } = this.state

    if (!_.includes(this.state.keywords, value)) {
      let keywords_ = keywords.concat([value])

      this.setState({ keywords: keywords_ })

      fetch(`/api/v1/schools?q=${keywords_.join(',')}`)
        .then(resp => resp.json())
        // There's also `count`, can be used to load next page
        .then(({ results }) => this.setState({ results }))
    }

    e.target.reset()
  }

  render() {
    const { keywords, results } = this.state

    return (
      <div>
        <form onSubmit={e => this.handleSearch(e)} className="pv2">
          <input name="query" type="text" placeholder="Search" autoComplete="off" />
          <div className="flex mt2">
            {keywords.map(kw => (
              <div key={kw} className="pa2 white bg-blue br1 mr2">{kw}</div>
            ))}
          </div>
        </form>
        <div className="pt2 bt b--light-gray">
          {results.map(school => (
            <div key={school.id} className="bb b--light-gray flex">
              <div className="w-50">
                <h2 className="f5">{school.name}</h2>
                <a href={school.website} target="_blank">{school.website}</a>
                <p>{school.address}</p>
              </div>
              <p className="p6">
                <strong>Type: </strong>{school.type}<br/>
                <strong>Session: </strong>{school.session}<br/>
                <strong>Main level: </strong>{school.main_level}<br/>
                <strong>Language: </strong>{school.language}<br/>
              </p>
            </div>
          ))}
        </div>
      </div>
    )
  }
}


ReactDOM.render(<Search />, document.querySelector('#search-placeholder'))
