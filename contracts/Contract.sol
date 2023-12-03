// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract queue
{
    struct Queue {
        uint256[] data;
        uint256 front;
        uint256 back;
    }

    function initializeQueue(Queue storage q) internal {
        q.data = new uint256[](100);
        q.front = 0;
        q.back = 0;
    }

    function push(Queue storage q, uint256 data) internal
    {
        if ((q.back + 1) % q.data.length == q.front)
            return; 
        q.data[q.back] = data;
        q.back = (q.back + 1) % q.data.length;
    }
    
    function pop(Queue storage q) internal
    {
        if (q.back == q.front)
            return ;
        delete q.data[q.front];
        q.front = (q.front + 1) % q.data.length;
    }
}

contract Complaint is queue{
    
    address public owner;
    address public officer1;
    address public officer2;
    address public officer3;
    uint256 public nextId;
    Queue public pendingApprovals;
    Queue public pendingActions;
    Queue public pendingResolutions;

    constructor(address _officer1, address _officer2, address _officer3) {
        owner = msg.sender;
        officer1 = _officer1;
        officer2 = _officer2;
        officer3 = _officer3;
        nextId = 1;
        initializeQueue(pendingApprovals);
        initializeQueue(pendingActions);
        initializeQueue(pendingResolutions);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner of this smart contract");
        _;
    }

    modifier onlyOfficer1() {
        require(
            msg.sender == officer1,
            "You are not the registered officer of this smart contract"
        );
        _;
    }

    modifier onlyOfficer2() {
        require(
            msg.sender == officer2,
            "You are not the registered officer of this smart contract"
        );
        _;
    }

    modifier onlyOfficer3() {
        require(
            msg.sender == officer3,
            "You are not the registered officer of this smart contract"
        );
        _;
    }

    struct complaint{
        uint256 id;
        address complaintRegisteredBy;
        string title;
        string description;
        string name;
        string department;
        string rollNumber;
        string approvalRemark;
        string actionRemark;
        string resolutionRemark;
        bool isApproved;
        bool isActionTaken;
        bool isResolved;
    }

    mapping(uint256 => complaint) public complaints;

    event ComplaintFiled(
        uint256 id,
        address complaintRegisteredBy,
        string title
    );

    function fileComplaint(
        string memory _title,
        string memory _description,
        string memory _name,
        string memory _department,
        string memory _rollNumber
    ) public {
        complaint storage newComplaint = complaints[nextId];
        newComplaint.id = nextId;
        newComplaint.complaintRegisteredBy = msg.sender;
        newComplaint.title = _title;
        newComplaint.description = _description;
        newComplaint.name = _name;
        newComplaint.department = _department;
        newComplaint.rollNumber = _rollNumber;
        newComplaint.approvalRemark = "Pending Approval";
        newComplaint.actionRemark = "Pending Action";
        newComplaint.resolutionRemark = "Pending Resolution";
        newComplaint.isApproved = false;
        newComplaint.isActionTaken = false;
        newComplaint.isResolved = false;
        push(pendingApprovals,newComplaint.id);
        emit ComplaintFiled(nextId, msg.sender, _title);
        nextId++;
    }

    function getPendingsReqs() public view returns (uint256){
        if(pendingApprovals.back == pendingApprovals.front){
            return 200;
        }else{
            return pendingApprovals.back - pendingApprovals.front;
        }
    }

    function getPendingsActions() public view returns (uint256){
        if(pendingActions.back == pendingActions.front){
            return 200;
        }else{
            return pendingActions.back - pendingActions.front;
        }
    }

    function getPendingsRes() public view returns (uint256){
        if(pendingResolutions.back == pendingResolutions.front){
            return 200;
        }else{
            return pendingResolutions.back - pendingResolutions.front;
        }
    }
    
    function getPendingReqComplaint() public view returns (complaint memory){
        require(pendingApprovals.back != pendingApprovals.front, "No Pending Complaints to Approve");
        uint256 _id = pendingApprovals.data[pendingApprovals.front];
        return complaints[_id];
    }

    function getPendingActionComplaint() public view returns (complaint memory){
        require(pendingActions.back != pendingActions.front, "No Pending Actions to Approve");
        uint256 _id = pendingActions.data[pendingActions.front];
        return complaints[_id];
    }

    function getPendingResComplaint() public view returns (complaint memory){
        require(pendingResolutions.back != pendingResolutions.front, "No Pending Actions to Approve");
        uint256 _id = pendingResolutions.data[pendingResolutions.front];
        return complaints[_id];
    }

    function approveComplaint(string memory _approvalRemark) public onlyOfficer1 {
        require(pendingApprovals.back != pendingApprovals.front, "No Pending Complaints to Approve");
        uint256 _id = pendingApprovals.data[pendingApprovals.front];
        require(complaints[_id].isApproved == false, "Complaint is already approved");
        complaints[_id].isApproved = true;
        complaints[_id].approvalRemark = _approvalRemark;
        push(pendingActions,_id);
        pop(pendingApprovals);
    }

    function disapproveComplaint(string memory _disapprovalRemark) public onlyOfficer1 {
        require(pendingApprovals.back != pendingApprovals.front, "No Pending Complaints to Approve");
        uint256 _id = pendingApprovals.data[pendingApprovals.front];
        require(complaints[_id].isApproved == false, "Complaint is already approved");
        complaints[_id].isApproved = false;
        complaints[_id].approvalRemark = string.concat("This complaint is rejected. Reason: ",_disapprovalRemark);
        pop(pendingApprovals);
    }

    function takeAction(string memory _actionRemark) public onlyOfficer2 {
        require(pendingActions.back != pendingActions.front, "No Pending Complaints to Take Action");
        uint256 _id = pendingActions.data[pendingActions.front];
        require(complaints[_id].isApproved == true, "Complaint is not yet approved");
        require(complaints[_id].isActionTaken == false, "Action is already taken for this complaint");
        complaints[_id].isActionTaken = true;
        complaints[_id].actionRemark = _actionRemark;
        push(pendingResolutions,_id);
        pop(pendingActions);
    }

    function resolveComplaint(string memory _resolutionRemark) public onlyOfficer3 {
        require(pendingResolutions.back != pendingResolutions.front, "No Pending Complaints to Resolve");
        uint256 _id = pendingResolutions.data[pendingResolutions.front];
        require(complaints[_id].isApproved == true, "Complaint is not yet approved");
        require(complaints[_id].isActionTaken == true, "Action is not yet taken for this complaint");
        require(complaints[_id].isResolved == false, "Complaint is already resolved");
        complaints[_id].isResolved = true;
        complaints[_id].resolutionRemark = _resolutionRemark;
        pop(pendingResolutions);
    }
    
    function setOfficerAddresses(address _officer1, address _officer2, address _officer3) public onlyOwner {
        officer1 = _officer1;
        officer2 = _officer2;
        officer3 = _officer3;
    }

    function getAllCases(address _sender) public view returns(complaint[] memory){
        uint256 count = 0;

        for (uint256 i = 1; i < nextId; i++) {
            if (complaints[i].complaintRegisteredBy == _sender) {
                count++;
            }
        }

        complaint[] memory userComplaints = new complaint[](count);

        count = 0;
        for (uint256 i = 1; i < nextId; i++) {
            if (complaints[i].complaintRegisteredBy == _sender) {
                userComplaints[count] = complaints[i];
                count++;
            }
        }

        return userComplaints;

    }
}