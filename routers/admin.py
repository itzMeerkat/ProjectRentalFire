from fastapi import APIRouter, Depends
import modules.db.firebaseapi as db

from modules.schema.data_schema import ChangeUserRole
from modules.rbac.rbac import AuthorizationFactory


router = APIRouter()

@router.post('/modifyuserrole')
async def set_frontdesk(request: ChangeUserRole, uid=Depends(AuthorizationFactory('user_claims', 'modify'))):
    user_ref = db.auth.get_user_by_email(request.user_email)
    db.auth.set_custom_user_claims(user_ref.uid, {'role': request.new_role})
    return {'res': True}

@router.post('/getongoing')
async def get_ongoing_activities(uid=Depends(AuthorizationFactory('activity', 'getall'))):
    return {'result': db.get_ongoing_activities()}

@router.get('/getalluser')
async def get_all_user():
    return {'result': fake_result }# db.get_all_user()}

null = []
fake_result = [
        {
            "uid": "0N5OeQsd0qYQyrxJ3UM2qkdIKb43",
            "email": "lala@gmail.com",
            "roles": null
        },
        {
            "uid": "234K6LDd6weilMEa2W4U7sfF1b63",
            "email": "heelo@gmail.com",
            "roles": null
        },
        {
            "uid": "2GCtcxVvXhbtQRcJShLaxM0DsIY2",
            "email": "aadila@ucdavis.edu",
            "roles": null
        },
        {
            "uid": "32iDHLNY4HN2A8dH2sHTniDxDOg2",
            "email": "testing@number100.com",
            "roles": null
        },
        {
            "uid": "3UImmvfoSBP21dmETE8HsqtwBmj1",
            "email": "w1708465@apps.losrios.edu",
            "roles": null
        },
        {
            "uid": "3Wt0n0epsqSWoqRR9K8fm5mI5bJ3",
            "email": "testing@number14.com",
            "roles": null
        },
        {
            "uid": "8oQJwO0OIhSPqwR38zaFAWz9e9a2",
            "email": "jagao@ucdavis.edu",
            "roles": null
        },
        {
            "uid": "9Egd92Fjm3bMcq0hvjXgdyfb2gj1",
            "email": "testing@number11.com",
            "roles": null
        },
        {
            "uid": "9zIWSP56vIgGUbtEhOZFhpm1J3u2",
            "email": "testing@number12.com",
            "roles": null
        },
        {
            "uid": "AXZ7VF04QPQBSa8Vt2M4I1uFNlY2",
            "email": "testing@number19.com",
            "roles": null
        },
        {
            "uid": "CcoiSpEZiTOnWv7CVf6bbQJEnA92",
            "email": "jagaoabc@gmail.com",
            "roles": null
        },
        {
            "uid": "CsytgY90ZFetbL1QK99XcWYsMD52",
            "email": "alle95liu@fmail.com",
            "roles": null
        },
        {
            "uid": "D3NnZvS2umPNY3GaqownDSfPVSR2",
            "email": "alle95liu@gmail.com",
            "roles": null
        },
        {
            "uid": "FC9u1Gqzj2bZQ25sC4ursI8x64s1",
            "email": "adila@ucdavis.edu",
            "roles": null
        },
        {
            "uid": "FtbLA2uSQvNY0oWGWJ4b08v9oEG2",
            "email": "testing@number9.com",
            "roles": null
        },
        {
            "uid": "GUUkK263mHMYTHXQArmP9v4a1pg2",
            "email": "testing@number1.com",
            "roles": null
        },
        {
            "uid": "JnSx2t2eyjVdhnlb5D94QAxqC5u2",
            "email": "testfrontdesk@mail.com",
            "roles": [
                "role"
            ]
        },
        {
            "uid": "Nt6lXRrKftQeajTBMEEaXRiSiWu1",
            "email": "testing@number90.com",
            "roles": null
        },
        {
            "uid": "Ob4vV6Teopd5EWJ2sPl8CMaN1WQ2",
            "email": "testing@number15.com",
            "roles": null
        },
        {
            "uid": "R5omIZYCd6dpcMW21zgHO0304953",
            "email": "jagaoabc2@gmail.com",
            "roles": null
        },
        {
            "uid": "RcFIgoKzMchWUA8WAlJinnHXf4w2",
            "email": "testing@number13.com",
            "roles": null
        },
        {
            "uid": "T0gQ1lNNLScWZoJBlUNXroyX6TI3",
            "email": "aleliu@ucdavis.edu",
            "roles": null
        },
        {
            "uid": "Ur4VehUfv0XYX5QnOaodyZWPZkw2",
            "email": "testing@number3.com",
            "roles": null
        },
        {
            "uid": "VW99I6t396R1R155QCOBPSaXm393",
            "email": "jagaoabc1@gmail.com",
            "roles": null
        },
        {
            "uid": "Wpnbbc3J7QQPqHJtrtOCIzQfQb13",
            "email": "heeloo@gmail.com",
            "roles": null
        },
        {
            "uid": "XrK5j6OjguMmCOoMxgURdfwHgR43",
            "email": "ladydilaa@gmail.com",
            "roles": null
        },
        {
            "uid": "Yf28ga5AJeZJiYEZ9VvpuzvuCOh2",
            "email": "testing@number1000.com",
            "roles": null
        },
        {
            "uid": "dRGRINoF1LV3IDgcuqAwuzvglTA3",
            "email": "testing@number5.com",
            "roles": null
        },
        {
            "uid": "edbaiweQDTQaaa8m2bc4woXTZiA2",
            "email": "testing@number10.com",
            "roles": null
        },
        {
            "uid": "lJvW5WDvNNbYwIO0UcyVaxb69Mw2",
            "email": "pkazhang@ucdavis.edu",
            "roles": null
        },
        {
            "uid": "r9eIU1XX42bgzEuDRERAw1TW6NG2",
            "email": "testing@number21.com",
            "roles": null
        },
        {
            "uid": "soTiza4m2MYbDCAbyfRbNgxQowH3",
            "email": "testemail@test.com",
            "roles": null
        },
        {
            "uid": "szrW7rIppETsOHcQ5DpQMNS8o1H2",
            "email": "testing@number20.com",
            "roles": null
        },
        {
            "uid": "tDjrJUIfPVcemIiYxyQyRlquK912",
            "email": "dila@ucdavis.edu",
            "roles": [
                "admin"
            ]
        }]

