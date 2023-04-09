const CosmosClient = require("@azure/cosmos").CosmosClient; // Import the CosmosDB SDK

const config = require("../../shared/config.js"); // Import the configuration file

const DATABASE_NAME = "AzureResume"; // Set the database name

const CONTAINER_NAME = "Counter"; // Set the container name

const PARTITION_KEY = "/id"; // Set the partition key

module.exports = async function (context, req) {
  // Export an async function as the entry point

  try {
    const client = new CosmosClient({
      // Create a new CosmosDB client instance

      endpoint: config.cosmos.endpoint, // Set the endpoint URL from configuration

      key: config.cosmos.key, // Set the access key from configuration
    });

    const database = client.database(DATABASE_NAME); // Get a reference to the database

    const container = database.container(CONTAINER_NAME); // Get a reference to the container

    const { resources: items } = await container.items // Query the container for items with the ID "counter"

      .query(`SELECT * FROM c WHERE c.id = "my_counter"`)

      .fetchAll();

    let item;

    if (items.length === 0) {
      // If no items are found, create a new item with a count of 1

      item = { id: "counter", count: 1 };

      await container.items.create(item);
    } else {
      // Otherwise, update the count property of the existing item

      item = items[0];

      item.count += 1;

      await container.items.upsert(item);
    }

    context.res = {
      // Set the response to return the current count as JSON

      status: 200,

      body: JSON.stringify({ count: item.count }),
    };
  } catch (error) {
    context.log.error(error); // Log any errors to the console

    context.res = {
      // Set the response to return a generic error message

      status: 500,

      body: "Internal Server Error",
    };
  }
};
