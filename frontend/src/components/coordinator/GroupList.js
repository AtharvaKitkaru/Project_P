import React from "react";
import { Link } from "react-router-dom";
import "./GroupList.scss";
import $ from "jquery";
// import GroupDetails from "./GroupDetails";
import GroupCardView from "./GroupCardView";
import GroupListView from "./GroupListView";
import saveCsv from "save-csv/save-csv.min.js";
import axios from "../../axios";

class GroupList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      viewType: "card",
    };
    // this.guides = [];
    // this.downloadable = [];
  }
  componentDidMount() {
    axios
      .get("coordinatorGroup/")
      .then(({ data }) => {
        console.log(data);

        this.setState({});
      })
      .catch((err) => console.log(err));
  }

  render() {
    return (
      <div className='groups mx-auto' style={{ width: "90%" }}>
        <br />

        <div
          className='p-2   text-center shadow-sm rounded font-weight-bold  mx-auto'
          style={{
            color: "rgb(183, 32, 46)",
            fontSize: "1.1em",
            width: "auto",
            backgroundColor: "rgba(231, 231, 231, 0.459)",
          }}>
          Select Group
        </div>
        <div className='d-flex my-4 '>
          {/* toggle view */}

          <div
            className='col-2 d-flex h-100  bg-white shadow-sm rounded p-0   my-auto'
            style={{
              color: "rgb(183, 32, 46)",
            }}>
            <div
              id='card'
              className='col-6 view-option text-center  bg-light p-1'
              onClick={() => {
                this.setState({ viewType: "card" }, () => {
                  $(".view-option").removeClass("bg-light");
                  $("#" + this.state.viewType).addClass("bg-light");
                });
              }}>
              <i className='fa fa-th ' aria-hidden='true'></i>
            </div>
            <div
              id='list'
              className='col-6  view-option text-center p-1'
              onClick={() => {
                this.setState({ viewType: "list" }, () => {
                  $(".view-option").removeClass("bg-light");
                  $("#" + this.state.viewType).addClass("bg-light");
                });
              }}>
              <i className='fa fa-list' aria-hidden='true'></i>
            </div>
          </div>
        </div>

        {/* toggle view ends here */}
        <div className='p-3'>
          {this.state.viewType === "card" ? (
            <GroupCardView />
          ) : (
            <GroupListView />
          )}
        </div>

        <br />
        <Link to='/groups'>
          <div className='mx-auto back-button p-2 text-center my-4 rounded-lg'>
            <i className='fa fa-arrow-down mr-2' aria-hidden='true' />
            Download
          </div>
        </Link>
      </div>
    );
  }
}
export default GroupList;
