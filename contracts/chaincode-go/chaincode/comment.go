package chaincode

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
	contractapi.Contract
}

type Asset struct {
	ID                  string    `json:"id"`
	Comment          	string    `json:"comment"`
	CommentUserCopy 	string    `json:"comment_user_copy"`
	CreatedAt           string 	  `json:"created_at"`
	AuthorID            string    `json:"author_id"`
	ComplaintID			string	  `json:"complaint_id`
}

// CreateAsset issues a new asset to the world state with given details.
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, id string, comment string, comment_user_copy string, complaint_id string, authorID string,created_at string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

	asset := Asset{
		ID:             		id,
		Comment:        		comment,
		CommentUserCopy:    	comment_user_copy,
		CreatedAt: 				created_at,
		AuthorID:				authorID,
		ComplaintID:			complaint_id,
	}
	assetJSON, err := json.Marshal(asset)

	if err != nil {
        return fmt.Errorf("joining error %s", err)
    }

	if err := ctx.GetStub().PutState(id, assetJSON); err != nil {
        return err
    }

	if err := s.CreateIndex(ctx, "complaint_id", []string{complaint_id, id}); err != nil {
        return err
    }

	return nil
}

func (s *SmartContract) CreateIndex(ctx contractapi.TransactionContextInterface, indexName string, attributes []string) error {
    indexKey, err := ctx.GetStub().CreateCompositeKey(indexName, attributes)
    if err != nil {
        return err
    }

    // Save index to the ledger
    return ctx.GetStub().PutState(indexKey, []byte{0x00})
}

func (s *SmartContract) QueryAssetsByComplaintID(ctx contractapi.TransactionContextInterface, complaint_id string) ([]*Asset, error) {
    resultsIterator, err := ctx.GetStub().GetStateByPartialCompositeKey("complaint_id", []string{complaint_id})
    if err != nil {
        return nil, err
    }
    defer resultsIterator.Close()

    var assets []*Asset
    for resultsIterator.HasNext() {
        queryResponse, err := resultsIterator.Next()
        if err != nil {
            return nil, err
        }

        // Retrieve asset ID from composite key
        _, compositeKeyParts, err := ctx.GetStub().SplitCompositeKey(queryResponse.Key)
        if err != nil {
            return nil, err
        }
        assetID := compositeKeyParts[1]

        // Retrieve asset details using asset ID
        asset, err := s.ReadAsset(ctx, assetID)
        if err != nil {
            return nil, err
        }

        assets = append(assets, asset)
    }

    return assets, nil
}


// ReadAsset returns the asset stored in the world state with given id.
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, id string) (*Asset, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}


// DeleteAsset deletes an given asset from the world state.
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, id string) error {
	exists, err := s.AssetExists(ctx, id)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", id)
	}

	return ctx.GetStub().DelState(id)
}


// GetAllAssets returns all assets found in world state
func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}
