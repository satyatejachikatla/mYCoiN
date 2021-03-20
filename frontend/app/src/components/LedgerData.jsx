import React, { Component } from "react";
import axios from "axios";

class LedgerData extends Component {
  state = { ledgerInfo: null, pendingTransactions: null };

  PrettyPrintJson = (data) => (
    <div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );

  render() {
    return <div>{this.PrettyPrintJson(this.state)}</div>;
  }

  componentDidMount() {
    axios.get("/show_data").then((res) => {
      const data = res.data;
      this.setState({ ledgerInfo: data.ledgerInfo });
      this.setState({ pendingLedgers: data.pendingLedgers });
      this.setState({ pendingTransactions: data.pendingTransactions });
    });
  }
}

export default LedgerData;
