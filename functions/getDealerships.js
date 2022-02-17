/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
/*
* Get all dealerships
* Get dealerships filtered by state
*/
const Cloudant = require('@cloudant/cloudant');
async function main(params) {
    const cloudant = Cloudant({
        url : params.COUCH_URL,
        plugins : { iamauth : {
            iamApiKey : params.IAM_API_KEY
        }}
    })
    
    if(params.state){
        try{
            let dealerships = await cloudant.db.use('dealerships').find({ "selector": { "st":params.state } })
			allDealershipsByState = dealerships.docs
			return { allDealershipsByState };
        }
        catch(error){
            return {error : error.description}
        }
    }
    else{
        try{
            let dealerships = await cloudant.db.use('dealerships').list({include_docs:true})
    		let allDealerships = []
    		dealerships.rows.forEach((dealership) => { allDealerships.push(dealership.doc) } )
    		return {allDealerships };
        }
        catch(error) {
            return {error : error.description}
        }
    }
    
}
