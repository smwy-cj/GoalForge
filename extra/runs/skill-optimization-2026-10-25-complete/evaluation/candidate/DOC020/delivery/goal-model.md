# 目标模型

版本：v1。人工待审。

- Receive recruiter emails during job applications.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Receive school news and notifications.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Review unread emails to identify important messages.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Mark important emails for attention.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Delete unwanted or spam emails to keep the inbox clear.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Read important emails.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Tag emails needing later action so the task can be completed when available.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Delete even important emails once their conversation has ended.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Separate important recruiting or school messages from deal mail using different email accounts.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Use an AI assistant to compose an email from the sender's main points.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Adjust font size when preparing an email.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Make important sentences bold before sending an email.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Send the prepared email.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Share multimedia through cloud links so recipients can view it on phones or laptops.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Avoid missing important messages due to spam classification, even at the cost of receiving some spam.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Edit a sent email rather than sending a separate correction.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Let recipients view the current edited email and optionally inspect its editing history.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Reliably receive expected emails such as website-registration messages.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Compose a well-organized email from brief input using an assistant built into the email client.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Warn before sending when the text says an attachment is present but the file is missing.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Use AI to extract the main points of received emails.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Highlight important keywords or details so the reader does not overlook them.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Avoid missing messages from recruiting teams.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Reduce the time spent reading every email.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Consider periodic summaries of batches of received emails as one way to reduce reading effort.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Receive notifications for important messages if importance detection is sufficiently reliable.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Forward email when coordinating work under a tight deadline.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Send a message to the whole group using bulk addressing or BCC under a tight deadline.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Search emails as an essential daily capability.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Filter messages by tags, including through search.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Schedule emails for different sending times.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Explore shared, self-defined email categories or protocol identifiers so correspondents can communicate using matching categories.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Maintain professional communication with people inside or outside one's employer.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Use email to book personal appointments such as dentist or clinic visits.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Receive merchandise sales or discount information by email.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Occasionally communicate with friends by email.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Adjust the AI-generated email draft before sending it.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.
- Reply to emails requiring a response when available.
  适用条件：This stakeholder and the described use case; no universal policy for all users is inferred.

## 目标之间的联系

下列联系不表示充分精化；待确认及已否定记录保留各自状态。

- 有依据的联系：Mark important emails for attention. —[有助于]→ Review unread emails to identify important messages.
  依据：Marking important messages helps triage but follows and does not itself perform the unread-message review.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Review unread emails to identify important messages. —[过程先后]→ Read important emails.
  依据：The respondent first glances over unread mail, then reads important messages in detail.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Tag emails needing later action so the task can be completed when available. —[过程先后]→ Reply to emails requiring a response when available.
  依据：When a reply cannot be done now, tagging records it before later completion.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Separate important recruiting or school messages from deal mail using different email accounts. —[有助于]→ Avoid missing messages from recruiting teams.
  依据：Separate accounts help isolate important recruiting or school mail, without ensuring delivery or attention.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Use an AI assistant to compose an email from the sender's main points. —[过程先后]→ Adjust the AI-generated email draft before sending it.
  依据：The described AI composition happens before the sender adjusts the output.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Adjust the AI-generated email draft before sending it. —[过程先后]→ Send the prepared email.
  依据：The sender adjusts content or formatting before sending.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Adjust font size when preparing an email. —[过程先后]→ Send the prepared email.
  依据：Font formatting is a described pre-send step, not a sufficient cause of sending.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Make important sentences bold before sending an email. —[过程先后]→ Send the prepared email.
  依据：Important sentences are made bold before the described send.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Avoid missing important messages due to spam classification, even at the cost of receiving some spam. —[有助于]→ Avoid missing messages from recruiting teams.
  依据：Avoiding erroneous spam placement helps avoid missed recruiting messages; missing mail can have other causes.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Compose a well-organized email from brief input using an assistant built into the email client. —[实现方式]→ Use an AI assistant to compose an email from the sender's main points.
  依据：A built-in assistant is explicitly proposed as a means to compose from short main-point input.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Use AI to extract the main points of received emails. —[有助于]→ Reduce the time spent reading every email.
  依据：Summarization is explicitly suggested to reduce the time spent reading every message.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Highlight important keywords or details so the reader does not overlook them. —[有助于]→ Read important emails.
  依据：Highlighting overlooked details supports careful reading but does not ensure understanding of the entire message.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Consider periodic summaries of batches of received emails as one way to reduce reading effort. —[实现方式]→ Reduce the time spent reading every email.
  依据：Periodic batch summaries are tentatively accepted as one way to reduce reading effort.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Receive notifications for important messages if importance detection is sufficiently reliable. —[有助于]→ Avoid missing messages from recruiting teams.
  依据：Reliable important-message alerts could reduce missed mail, with the acknowledged failure condition if detection misses an item.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.
- 有依据的联系：Search emails as an essential daily capability. —[实现方式]→ Filter messages by tags, including through search.
  依据：The respondent says tag filtering can be done through searching; searching is the proposed means to obtain the filtered messages.
  条件／假设：Only in the source-described scenario; endpoint conditions and defeasible preferences remain applicable.

## 需要确认

- Joint sufficiency is unconfirmed: Conservative spam handling, reliable alerts and separated accounts can help; the speaker expressly declines reliance when AI can miss importance.
- Joint sufficiency is unconfirmed: Summaries, highlighting and a tentative batch digest may reduce reading effort but accuracy and completeness are unproven.
- 这组层级仍需确认，尚未作为成立的精化展示。
- 这组层级仍需确认，尚未作为成立的精化展示。
- Only the provided native-text interview was available; audio and actual application behavior were not independently checked.
- One assistant authored extraction, support judgments and model decisions in shared within-document context; this is not independent semantic review or formal proof.

原文与层级依据可在 HTML 中展开。结构检查不等于语义证明，意见导出后交回助手。
