Challenge Summary

Imagine you're a data engineer at a "digital wallet" company called PayMo that allows users to easily request and make payments to other PayMo users. The team at PayMo has decided they want to implement features to prevent fraudulent payment requests from untrusted users.
Feature 1

When anyone makes a payment to another user, they'll be notified if they've never made a transaction with that user before.

    "unverified: You've never had a transaction with this user before. Are you sure you would like to proceed with this payment?"

Feature 2

The PayMo team is concerned that these warnings could be annoying because there are many users who haven't had transactions, but are still in similar social networks.

For example, User A has never had a transaction with User B, but both User A and User B have made transactions with User C, so User B is considered a "friend of a friend" for User A.

For this reason, User A and User B should be able to pay each other without triggering a warning notification since they're "2nd degree" friends.

To account for this, PayMo would like you to also implement this feature. When users make a payment, they'll be notified when the other user is outside of their "2nd-degree network".

    "unverified: This user is not a friend or a "friend of a friend". Are you sure you would like to proceed with this payment?"

Feature 3

More generally, PayMo would like to extend this feature to larger social networks. Implement a feature to warn users only when they're outside the "4th degree friends network".

In the above diagram, payments have transpired between User

    A and B
    B and C
    C and D
    D and E
    E and F

Under this feature, if User A were to pay User E, there would be no warning since they are "4th degree friends".

However, if User A were to pay User F, a warning would be triggered as their transaction is outside of the "4th-degree friends network."

(Note that if User A were to pay User C instead, there would be no warning as they are "2nd-degree" friends and within the "4th degree network")
Other considerations and optional features

It's critical that these features don't take too long to run. For example, if it took 5 seconds when you make a payment to check whether a user is in your network, that would ruin your user experience and wouldn't be acceptable.

While PayMo is a fictional company, the dataset is quite interesting -- it's inspired by a real social network, includes the time of transaction, and the messages come from real Venmo transactions -- so feel free to implement additional features that might be useful to prevent fraudulent payments.
