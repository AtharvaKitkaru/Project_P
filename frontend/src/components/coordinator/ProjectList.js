import React from "react";
import { Redirect, Link } from "react-router-dom";
import "./ProjectList.scss";
import saveCsv from "save-csv/save-csv.min.js";
import axios from "../../axios";

class ProjectList extends React.Component {
  constructor(props) {
    super(props);
    this.projects = [];
    this.downloadable = [];
  }
  componentDidMount() {
    axios.get("coordinatorProject/").then(({ data }) => {
      console.log(data);
      this.projects = data;
      this.downloadable.push(
        this.projects.map((project) => {
          return {
            project_id: project.project_id,
            project_name: project.project_name,
            group_id: project.group_id,
            guide_name: project.guide_name,
            project_domain: project.project_domain,
            guide_name: project.guide_name,
            project_category: project.project_category,
            project_description: project.project_description,
            project_explanatory_field: project.project_explanatory_field,
          };
        }),
      );
      console.log(this.downloadable);
      this.setState({});
    });
  }

  render() {
    return (
      <div className='project mx-auto' style={{ width: "90%" }}>
        <br />
        <div
          className='p-2 px-3 text-center shadow-sm rounded font-weight-bold'
          style={{
            color: "rgb(183, 32, 46)",
            fontSize: "1.1em",
            backgroundColor: "rgba(231, 231, 231, 0.459)",
          }}>
          Project List
        </div>

        <div class='table-responsive-sm'>
          <table class='ui striped table'>
            <thead class='text-center'>
              <tr class=''>
                <th class='' scope='col'>
                  Projec
                  t Name
                </th>
                <th class='' scope='col'>
                  Guide Name
                </th>
                <th class='' scope='col'>
                  Group Number
                </th>
                <th class='' scope='col'>
                  Domain
                </th>
              </tr>
            </thead>
            <tbody class='text-center'>
              {this.projects.length &&
                this.projects.map((project) => (
                  <tr
                    class=''
                    onClick={() =>
                      this.props.history.push(`/project/${project.project_id}`)
                    }>
                    <td class=''>{project.project_title}</td>
                    <td class=''>{project.guide_name}</td>
                    <td class=''>{project.group_id}</td>
                    <td class=''>{project.project_domain}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
        <div className='w-100 d-flex justify-content-center'>
          <div
            className='btn btn-danger'
            onClick={() =>
              saveCsv(this.downloadable[0], {
                filename: "project-list.csv",
              })
            }>
            <i className='fa fa-arrow-down mr-2' />
            Download
          </div>
        </div>
      </div>
    );
  }
}
export default ProjectList;
