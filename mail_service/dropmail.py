import secrets 
import uuid
from string import Template
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class mail_handler:
	def __init__(self, tg_id, id=""):
		self.id=id
		self.AUTH_TOKEN =  tg_id
		self.transport = RequestsHTTPTransport(url=f"https://dropmail.me/api/graphql/{self.AUTH_TOKEN}") 
		self.client = Client(transport=self.transport, fetch_schema_from_transport=True) 

	def get_mail(self):
		query = gql(Template(""" {
			session(id: "$id") {
				mails{
					rawSize,
					fromAddr,
					toAddr,
					downloadUrl,
					text,
					headerSubject
					}
				}
			}""").safe_substitute(id=self.id))
		result = self.client.execute(query)
		print(result)
		return result

	def new_mailbox(self):
		query = gql(
			"""
			mutation {
				introduceSession {
					id,
					expiresAt,
					addresses {
					address
					}
				}
			}
		"""
		)

		# Execute the query on the transport
		result = self.client.execute(query)
		return result


if __name__ == '__main__':
	# Select your transport with a defined url endpoint
	mail = mail_handler("281048238", "U2Vzc2lvbjpjx4KfWmdCboX1Me373qBr")
	letters = mail.get_mail()
	answer = letters 
	print(answer)

