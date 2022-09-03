# StoriHomeTest

## Technology Stack
- Python (Flask)
- MongoDB

While technically the challenge behavior can be achieved through simple python scripts (So they can run in a cron job, for example), I went with an API approach so it's closer to an actual, scalable implementation of a Transactions System.

## Requirements
- Docker Engine and Docker Compose (Development made on v20.10.11)
- Browser, Postman or any preferred tool to make API requests

## How to Execute
1. Run:
```
docker-compose build
docker-compose up
```
2. In your request tool, send a GET request to [Load Data Endpoint](localhost:5000/load_transactions)
3. Now you can send a request to either [View Summary](localhost:5000/view_summary) or [Send Email](localhost:5000/send_email)
4. If you sent a request to **Send Email**, you will need to access [Mailtrap](mailtrap.io) to see the email. Mailtrap is being used to allow easier access to the email, since Gmail no longer supports ["Less Secure Apps"](https://support.google.com/accounts/answer/6010255?hl=en#zippy=%2Cuse-an-app-password).

The credentials for Mailtrap are:
```
email: anastorihometest@gmail.com
password: storihometest123
```
5. Once you login, enter "My Inbox" and you should be able to see the received emails there.
6. If you sent a request to **View Summary** an email WILL NOT BE RECEIVED, view summary is just an extra endpoint to visualize the summary in JSON format. 

## Definitions:
Based off the example included in the PDF received for the Challenge Statement:
- **Total Balance** = Sum of all transaction amounts (Both debit - represented by negative amounts, and credit - represented by positive amounts)
- **Average Debit Amount (Historical)** - Average of all the Debit (negative) Transactions.
- **Average Credit Amount (Historical)** - Average of all the Credit (positive) Transactions.
- **Average Debit Amount (Monthly Details)** - Average of the Debit Transactions of the corresponding month only.
- **Average Credit Amount (Monthly Details)** - Average of the Credit Transactions of the corresponding month only.

## Assumptions and Must Knows:
- The date of each transaction consist of MM/DD only (Based off the example included in the PDF).
- For month, values 1-12 are admited. 
- For day, values 1-31 are admitted. There's no validation yet for which days have 30 or 31 days.
- For an amount to be valid, a + or - sign must be present at char[0]
- Decimals for totals obtained are set to a precision of 2 decimals, rounded.
- For an amount from the csv to be valid, it must contain 2 decimal digits.

## Aspects that Could Be Improved in Next Iteration:
- Make Exception Handling more specific, through custom exceptions.
- Add unit and integration testing - Not added yet due to time constraints.
- Host API and DB in AWS instead of locally - Not added yet due to time constraints.
- Create an OpenAPI interface for endpoint Documentation.