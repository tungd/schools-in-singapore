import React, { Component } from 'react'
import ReactDOM from 'react-dom'


class Search extends Component {

  render() {
    return (
      <h1>Search</h1>
    )
  }
}


ReactDOM.render(<Search />, document.querySelector('#search-placeholder'))
